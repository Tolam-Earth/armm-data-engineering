import pandas as pd

CATEGORICAL_COLUMNS = ['country', 'project_category', 'project_type']


def generate_categorypool_list(data: pd.DataFrame) -> list:
    categorypool_list = []
    for categorypool_name in CATEGORICAL_COLUMNS:
        temp = sorted(data[categorypool_name].unique().tolist())
        categorypool_list.extend(temp)
    return categorypool_list


def generate_pool_name(categorypool_list: list, pool_id: str) -> str:
    """ generates a pool name by concatenating categories and pool id separated by underscores """
    return "_".join([*categorypool_list, pool_id])
