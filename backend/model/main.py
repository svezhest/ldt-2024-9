from typing import Optional
from backend.types.workload import Workload, WorkloadType


def predict(workload_type: Optional[WorkloadType]) -> list[Workload]:
    '''
    Предсказывает количество исследований.
    В зависимости от реализации, можем указывать тип исследований, а можем и предсказывать всё сразу.
    '''
    df = get_data(workload_type)
    pass


def get_data(workload_type: Optional[WorkloadType]) -> any:
    '''
    Делает запрос в БД и отдает данные в виде, подходящем для модели.
    '''
    pass


def update_data(new_data: list[Workload]):
    '''
    Добавляет новые данные в БД.
    '''
    pass
