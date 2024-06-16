import datetime
import enum

import pandas as pd

from api_v1.workload.workload import WorkloadType
from logic.calculate_schedule import is_day_off
from logic.date_decomposition import year_and_week_number_to_date

if __name__ == '__main__':
    from catboost import CatBoostRegressor
    from xgboost import XGBRFRegressor
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

from logic.predict import mapping_back
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error

class Season(str, enum.Enum):
    WINTER = 'winter'
    SUMMER = 'summer'
    FALL = 'fall'
    SPRING = 'spring'


mapping = {
    1: Season.WINTER,
    2: Season.WINTER,
    3: Season.SPRING,
    4: Season.SPRING,
    5: Season.SPRING,
    6: Season.SUMMER,
    7: Season.SUMMER,
    8: Season.SUMMER,
    9: Season.FALL,
    10: Season.FALL,
    11: Season.FALL,
    12: Season.WINTER,
}


def get_amount_of_workdays_in_week(year: int, week_number: int) -> int:
    start_date = year_and_week_number_to_date(year, week_number)
    end_date = start_date + datetime.timedelta(days=7)

    res = 0

    date = start_date
    while date != end_date:
        res += 0 if is_day_off(date.date()) else 1
        date += datetime.timedelta(days=1)

    return res

def get_amount_of_workdays_in_week_before(year: int, week_number: int) -> int:
    start_date = year_and_week_number_to_date(year, week_number) + datetime.timedelta(days=-7)
    end_date = start_date + datetime.timedelta(days=7)

    res = 0

    date = start_date
    while date != end_date:
        res += 0 if is_day_off(date.date()) else 1
        date += datetime.timedelta(days=1)

    return res

def get_amount_of_workdays_in_month(year: int, week_number: int) -> int:
    start_date = year_and_week_number_to_date(year, week_number)
    start_date += datetime.timedelta(days=-start_date.day)
    end_date = (start_date.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
 
    res = 0

    date = start_date
    while date != end_date:
        res += 0 if is_day_off(date.date()) else 1
        date += datetime.timedelta(days=1)

    return res


def month_to_season(month: int):
    return mapping[month]


def train():
    df = pd.read_excel('data.xlsx')

    df.fillna(0, inplace=True)

    date_col = df.apply(lambda row: year_and_week_number_to_date(
        int(row['Год']), int(row['Номер недели'])), axis=1)

    df['month'] = date_col.apply(lambda d: d.month)
    df['season'] = df['month'].apply(month_to_season)
    df['total_workdays'] = df.apply(lambda row: get_amount_of_workdays_in_week(
        int(row['Год']), int(row['Номер недели'])), axis=1)

    df['total_workdays_prev_week'] = df.apply(lambda row: get_amount_of_workdays_in_week_before(
        int(row['Год']), int(row['Номер недели'])), axis=1)
    
    df['total_workdays_this_month'] = df.apply(lambda row: get_amount_of_workdays_in_month(
        int(row['Год']), int(row['Номер недели'])), axis=1)

    df['day_of_year'] = date_col.apply(lambda d: d.timetuple().tm_yday)

    df = pd.get_dummies(df, columns=['season'])

    X = df[['Год', 'Номер недели', 'month',] + [col for col in df.columns if 'season_' in col]]

    model1 = CatBoostRegressor(verbose=False)
    model2 = GradientBoostingRegressor(n_estimators=200, max_depth=5, min_samples_leaf=2, learning_rate=0.2)
    model3 = XGBRFRegressor()
    model4 = RandomForestRegressor()

    for model in (model1, model2, model3, model4):
        print('===', model.__class__)
        for workload_type in WorkloadType:
            cyrillic = mapping_back[workload_type]

            y = df[cyrillic]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(4) / 109, shuffle=False)

            # model = CatBoostRegressor(verbose=False)
            # model = GradientBoostingRegressor()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            err = mean_absolute_percentage_error(y_test, y_pred)

            # print(y_test.tolist(), y_pred)
            print(workload_type, err)

if __name__ == '__main__':
    train()

# === <class 'xgboost.sklearn.XGBRFRegressor'>
# WorkloadType.DENSITOMETER 1.7552144612265466
# WorkloadType.CT 1.2948522507670717
# WorkloadType.CT_CONTRAST 0.7615271876114053
# WorkloadType.CT_CONTRAST_MULTI 0.5726129612107907
# WorkloadType.MMG 0.7133644894529745
# WorkloadType.MRI 0.4089094152011886
# WorkloadType.MRI_CONTRAST 0.3247463449458122
# WorkloadType.MRI_CONTRAST_MULTI 0.9646463779842153
# WorkloadType.RG 0.5660607120586251
# WorkloadType.FLUOROGRAPHY 20.824309405684314
