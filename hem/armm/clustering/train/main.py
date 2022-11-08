import joblib
import argparse
import pandas as pd
import numpy as np

from hem.armm.clustering.model.pipelinemodel import pipeline
from hem.armm.clustering.model.gridsearch import gridsearch
from hem.armm.clustering.train.helper import generate_categorypool_list, generate_pool_name


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_address", type=str, help="the address to the csv file containing the training data")
    parser.add_argument("--n_splits", help="number of folds for k-fold cross-validation", type=int, default=5)
    parser.add_argument("--n_init",
                        help="number of times the clustering algorithm will run with different centroid initialization",
                        type=int, default=1)
    parser.add_argument("--n_jobs",
                        help="number of jobs to run in parallel with gridsearch algorithm",
                        type=int, default=-1)
    parser.add_argument("--pooling_version",
                        help="Version of the pooling model",
                        type=str, default="0.0.0.0")
    args = parser.parse_args()
    return args.data_address, args.n_splits, args.n_init, args.n_jobs, args.pooling_version


def train_final_model(data: pd.DataFrame, n_clusters: int, n_init: int, pooling_version: str = "0.0.0.0") -> pipeline:
    """
    :param data: the pandas DataFrame containing the training data
    :param n_clusters: number of clusters/centroids in the model
    :param n_init: number of times the clustering algorithm will run with different centroid initialization
    :param pooling_version: a str to be recorded as the model's version

    :return: trained pipeline
    """
    model = pipeline(pooling_version=pooling_version, n_clusters=n_clusters, n_init=n_init)
    model.fit(data)
    labels = model.predict(data)
    pool_ids = np.array([model['clustering']._label_uuid_dict[_label] for _label in labels])
    for id_ in np.unique(pool_ids):
        model['clustering']._uuid_categorypool_dict[id_] = generate_categorypool_list(
            data.loc[pool_ids == id_])  # to record category pool
        model['clustering']._uuid_poolname_dict[id_] = generate_pool_name(
            model['clustering']._uuid_categorypool_dict[id_], pool_id=id_)  # to record pool names
    return model


def main(data: pd.DataFrame, n_splits: int = 5, n_init: int = 1, n_jobs: int = -1,
         pooling_version: str = "0.0.0.0") -> pipeline:
    """
    :param data: the pandas DataFrame containing the training data
    :param n_splits: number of folds for k-fold cross-validation
    :param n_init: number of times the clustering algorithm will run with different centroid initialization
    :param n_jobs: number of jobs to run in parallel with gridsearch algorithm
    :param pooling_version: a str to be recorded as the model's version

    :return: trained pipeline
    """
    min_n_clusters = len(data['project_type'].unique())
    # max_n_clusters = int(data.groupby(by=['country', 'project_type']).ngroups)
    max_n_clusters = 5 * min_n_clusters

    optimal_n_clusters = gridsearch(data=data, min_n_clusters=min_n_clusters,
                                    max_n_clusters=max_n_clusters, n_splits=n_splits, n_init=n_init,
                                    n_jobs=n_jobs)
    return train_final_model(data=data, n_clusters=optimal_n_clusters, n_init=n_init, pooling_version=pooling_version)


if __name__ == '__main__':
    data_address, n_splits, n_init, n_jobs, pooling_version = get_arguments()
    data = pd.read_csv(data_address)
    model = main(data=data, n_splits=n_splits, n_init=n_init, n_jobs=n_jobs, pooling_version=pooling_version)
    # saves: the model as pkl file
    joblib.dump(model, 'model.pkl')
