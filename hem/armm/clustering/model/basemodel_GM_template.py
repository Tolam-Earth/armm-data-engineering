from uuid import uuid4
from sklearn.mixture import GaussianMixture
from sklearn.metrics import calinski_harabasz_score

# necessary for pipeline and gridsearch to define input params as keywords
BASEMODEL_N_CLUSTERS_NAME = "n_components"


class BaseModel(GaussianMixture):
    def __init__(self, n_components: int = 2, n_init: int = 1, **kwargs):
        """
        :param n_components: number of clusters to form as well as the number of centroids to generate
        :param n_init: number of times the clustering algorithm will be run with different centroid initialization
        :param **kwargs: passing kwargs to GaussianMixture.__init__()
        """
        super(BaseModel, self).__init__(n_components=n_components, n_init=n_init, **kwargs)
        self._label_uuid_dict = {_label: str(uuid4()) for _label in range(n_components)}
        self._uuid_poolname_dict = {}  # to record pool names during training creations
        self._uuid_categorypool_dict = {}  # a dict to record category pool (list) during training creations

    def score(self, x, y=None, **keywords):
        labels = self.predict(x)
        return calinski_harabasz_score(x, labels)
