import argparse
import pandas as pd
import numpy as np

from hem.armm.clustering.predict.loadmodel import loadmodel


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_address", type=str, help="the address to the trained pipeline")
    parser.add_argument("data_address", type=str, help="the address to the csv file containing the test data")
    args = parser.parse_args()
    return args.model_address, args.data_address


def main(model, data: pd.DataFrame) -> pd.DataFrame:
    """
    :param model: either a trained pipeline or the address to the trained pipeline
    :param data: the pandas DataFrame containing the test data

    :return: data with an additional column token_pool_id column
    """
    if isinstance(model, str):
        model = loadmodel(model_address=model)
    labels = model.predict(data)
    labels = [model['clustering']._label_uuid_dict[_label] for _label in labels]
    data['token_pool_id'] = labels
    data['name_pool'] = [model['clustering']._uuid_poolname_dict[_label] for _label in labels]
    data['pooling_version'] = np.repeat([model.pooling_version], len(labels))
    return data


if __name__ == '__main__':
    model_address, data_address = get_arguments()
    model = loadmodel(model_address=model_address)
    data = pd.read_csv(data_address)
    data = main(model=model, data=data)
    # saves: the labeled test data as .csv file
    data.to_csv('clustered-data.csv', index=False)
