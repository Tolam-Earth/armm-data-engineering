import json
import time
import argparse
import pandas as pd

from hem.armm.clustering.predict.loadmodel import loadmodel


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_address", type=str, help="the address to the trained pipeline")
    parser.add_argument("data_address", type=str, help="the address to the csv file containing the labeled data")
    parser.add_argument("dt_pool", type=int, help="Datetime stamp of when the pool was created")
    args = parser.parse_args()
    return args.model_address, args.data_address, args.dt_pool


def main(model, data: pd.DataFrame, dt_pool: int) -> list:
    """

    :param model: the trained pipeline
    :param data: the pandas DataFrame containing the labeled data

    :return: data: input data with an additional column token_pool_id column, pool_meta the
    :return: pool_meta: the token pool metadata table
    """
    if isinstance(model, str):
        model = loadmodel(model_address=model)
    pool_meta = []
    for token_pool_id in data['token_pool_id'].unique():
        temp = {'version_pool': model.pooling_version, 'dt_pool': dt_pool, 'id': token_pool_id}
        temp['attributes_pool'] = model['preprocessing'].attributes_pool
        temp['category_pool'] = model['clustering']._uuid_categorypool_dict[token_pool_id]
        temp['name_pool'] = model['clustering']._uuid_poolname_dict[token_pool_id]
        pool_data_transformed = model['preprocessing'].transform(data.loc[data.token_pool_id == token_pool_id])
        temp['mean_pool'] = pool_data_transformed.mean().values.tolist()
        temp['median_pool'] = pool_data_transformed.median().values.tolist()
        temp['var_pool'] = pool_data_transformed.var().values.tolist()
        temp['stdev_pool'] = pool_data_transformed.std().values.tolist()
        temp['n_pool'] = len(pool_data_transformed)
        pool_meta.append(temp)
    return pool_meta


if __name__ == '__main__':
    model_address, data_address, dt_pool = get_arguments()
    model = loadmodel(model_address=model_address)
    data = pd.read_csv(data_address)
    pool_meta = main(model, data, dt_pool)
    with open('pool_meta.json', 'w') as file:
        json.dump(pool_meta, file, indent=4)
