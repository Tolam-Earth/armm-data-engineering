
# Copyright (c) 2022 Tolam Earth
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import pandas as pd
from sklearn.model_selection import GridSearchCV

from hem.armm.clustering.model.basemodel_GM_template import BASEMODEL_N_CLUSTERS_NAME
from hem.armm.clustering.model.pipelinemodel import pipeline


def gridsearch(data: pd.DataFrame, min_n_clusters: int, max_n_clusters: int,
               n_splits: int = 5, n_init: int = 1, n_jobs: int = -1) -> int:
    """

    :param data: pandas.dataframe used for optimization of n_clusters
    :param min_n_clusters: minimum n of clusters in optimization
    :param max_n_clusters: maximum n of clusters in optimization
    :param n_splits: number of folds for k-fold cross-validation
    :param n_init: number of times the clustering algorithm will be run with different centroid initialization
    :param n_jobs: number of jobs to run in parallel with gridsearch algorithm

    :return: the optimal number of clusters as integer
    """
    model = pipeline(n_init=n_init)
    param_grid = {f"clustering__{BASEMODEL_N_CLUSTERS_NAME}": range(min_n_clusters, max_n_clusters + 1)}

    gcv = GridSearchCV(model, param_grid, n_jobs=n_jobs, cv=n_splits, pre_dispatch='2*n_jobs', refit=False)
    gcv.fit(data)
    return int(gcv.best_params_[f"clustering__{BASEMODEL_N_CLUSTERS_NAME}"])
