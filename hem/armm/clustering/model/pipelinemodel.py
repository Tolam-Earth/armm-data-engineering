
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

from sklearn.pipeline import Pipeline

from hem.armm.clustering.model.basemodel_GM_template import BaseModel, BASEMODEL_N_CLUSTERS_NAME
from hem.armm.clustering.preprocessing.preprocessing import Preprocessor


class pipeline_versioned(Pipeline):
    def __init__(self, steps, pooling_version: str = '0.0.0.0', **kwargs):
        super(pipeline_versioned, self).__init__(steps=steps, **kwargs)
        self.pooling_version = pooling_version


def pipeline(pooling_version='0.0.0.0', **kwargs) -> Pipeline:
    if 'n_clusters' in kwargs:
        kwargs[BASEMODEL_N_CLUSTERS_NAME] = kwargs.pop('n_clusters')
    return pipeline_versioned(pooling_version=pooling_version,
                              steps=[('preprocessing', Preprocessor()), ('clustering', BaseModel(**kwargs))])
