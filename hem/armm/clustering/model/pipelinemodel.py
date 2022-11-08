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
