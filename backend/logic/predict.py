from collections import defaultdict
import math
from api_v1.workload.workload import WorkloadType
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import chardet
import warnings
warnings.filterwarnings("ignore")



dummy = {
    WorkloadType.DENSITOMETER: 1329,
    WorkloadType.CT: 4882,
    WorkloadType.CT_CONTRAST: 544,
    WorkloadType.CT_CONTRAST_MULTI: 612,
    WorkloadType.MMG: 14002,
    WorkloadType.MRI: 1957,
    WorkloadType.MRI_CONTRAST: 792,
    WorkloadType.MRI_CONTRAST_MULTI: 8,
    WorkloadType.RG: 57966,
    WorkloadType.FLUOROGRAPHY: 18959,

}

predictions = None


def predict(year: int, week_number: int) -> dict[WorkloadType, int]:
    update_predictions(year, week_number)
    
    if (year, week_number) not in predictions:
        return dummy
    
    return predictions[(year, week_number)]


mapping = {
    'Денситометр': WorkloadType.DENSITOMETER,
    'КТ': WorkloadType.CT,
    'КТ с КУ 1 зона': WorkloadType.CT_CONTRAST,
    'КТ с КУ 2 и более зон': WorkloadType.CT_CONTRAST_MULTI,
    'ММГ': WorkloadType.MMG,
    'МРТ': WorkloadType.MRI,
    'МРТ с КУ 1 зона': WorkloadType.MRI_CONTRAST,
    'МРТ с КУ 2 и более зон': WorkloadType.MRI_CONTRAST_MULTI,
    'РГ': WorkloadType.RG,
    'Флюорограф': WorkloadType.FLUOROGRAPHY,
}


def update_predictions(year: int, week_number: int):
    global predictions

    steps = (year - 2024) * 52 + week_number

    if predictions is None or (year, week_number) not in predictions:
        _predictions = run_prediction(steps)

        predictions = {}

        for _prediction in _predictions:
            _year = _prediction['Год']
            _week_number = _prediction['Номер недели']
            workload_type = mapping[_prediction['Тип исследования']]
            amount: float = _prediction['Количество исследований']

            if (_year, _week_number) not in predictions:
                predictions[(_year, _week_number)] = defaultdict(int)

            predictions[(_year, _week_number)][workload_type] = math.ceil(amount)


def run_prediction(steps: int = 4) -> list:
    file_path = 'data.csv' 

    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    df = pd.read_csv(file_path, encoding=encoding, sep=',')

    if 'Год' not in df.columns or 'Номер недели' not in df.columns:
        raise KeyError("Отсутствуют необходимые столбцы 'Год' и 'Номер недели'.")


    df['Дата'] = pd.to_datetime(df['Год'].astype(str) + '-W' + df['Номер недели'].astype(str) + '-1', format='%G-W%V-%u', errors='coerce')
    df = df.dropna(subset=['Дата'])
    df = df[df['Дата'].dt.year >= 2022]  
    df.set_index('Дата', inplace=True)

    grouped = df[['КТ', 'КТ с КУ 1 зона', 'КТ с КУ 2 и более зон', 'ММГ', 'МРТ', 'МРТ с КУ 1 зона', 'МРТ с КУ 2 и более зон', 'РГ', 'Флюорограф']]

    best_params = {
        'КТ': {'order': (1, 1, 1), 'seasonal_order': (1, 1, 1, 52)},
        'КТ с КУ 1 зона': {'order': (1, 0, 1), 'seasonal_order': (1, 1, 0, 52)},
        'КТ с КУ 2 и более зон': {'order': (2, 1, 2), 'seasonal_order': (0, 1, 1, 52)},
        'ММГ': {'order': (1, 1, 0), 'seasonal_order': (1, 0, 1, 52)},
        'МРТ': {'order': (0, 1, 1), 'seasonal_order': (1, 1, 1, 52)},
        'МРТ с КУ 1 зона': {'order': (1, 0, 2), 'seasonal_order': (1, 1, 0, 52)},
        'МРТ с КУ 2 и более зон': {'order': (2, 1, 1), 'seasonal_order': (1, 1, 1, 52)},
        'РГ': {'order': (1, 1, 1), 'seasonal_order': (0, 1, 1, 52)},
        'Флюорограф': {'order': (1, 0, 1), 'seasonal_order': (1, 1, 0, 52)}
    }

    forecasts = {}

    for column in grouped.columns:
        group = grouped[[column]].dropna()
        
        if len(group) < 10: 
            continue
        
        params = best_params.get(column, None)
        if params is None:
            continue
        
        order = params['order']
        seasonal_order = params['seasonal_order']
        
        try:
            model = SARIMAX(group[column], order=order, seasonal_order=seasonal_order)
            results = model.fit(disp=False)
            forecast = results.get_forecast(steps=steps)
            
            forecasts[column] = forecast.predicted_mean
            
        except Exception as e:
            print(f"Не удалось построить модель для")

    if forecasts:
        forecast_df = pd.DataFrame(forecasts)
        forecast_df = forecast_df.reset_index()
        forecast_df['index'] = pd.to_datetime(forecast_df['index'])  
        forecast_df = forecast_df[forecast_df['index'].dt.year > 2022]  
        forecast_df['Год'] = forecast_df['index'].dt.year
        forecast_df['Номер недели'] = forecast_df['index'].dt.isocalendar().week

        forecast_melted = forecast_df.melt(id_vars=['Год', 'Номер недели'], var_name='Тип исследования', value_name='Количество исследований')

        forecast_melted = forecast_melted.dropna(subset=['Количество исследований'])

        forecast_melted = forecast_melted[~forecast_melted['Количество исследований'].apply(lambda x: isinstance(x, pd.Timestamp))]

        forecast_melted = forecast_melted.sort_values(by=['Год', 'Номер недели']).reset_index(drop=True)

        forecast_list = forecast_melted.to_dict(orient='records')

        return forecast_list