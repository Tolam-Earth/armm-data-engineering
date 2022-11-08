from uuid import uuid4
from sklearn.cluster import BisectingKMeans
from sklearn.metrics import calinski_harabasz_score

# necessary for pipeline and gridsearch to define input params as keywords
BASEMODEL_N_CLUSTERS_NAME = "n_clusters"


class BaseModel(BisectingKMeans):
    def __init__(self, n_clusters: int = 2, n_init: int = 1, **kwargs):
        """
        :param n_clusters: number of clusters to form as well as the number of centroids to generate
        :param n_init: number of times the clustering algorithm will be run with different centroid initialization
        :param **kwargs: passing kwargs to BisectingKMeans.__init__()
        """
        super(BaseModel, self).__init__(n_clusters=n_clusters, n_init=n_init, **kwargs)
        self._label_uuid_dict = {_label: str(uuid4()) for _label in range(n_clusters)}
        self._uuid_poolname_dict = {}  # to record pool names during training creations
        self._uuid_categorypool_dict = {}  # a dict to record category pool (list) during training creations

    def score(self, x, y=None, **keywords):
        labels = self.predict(x)
        return calinski_harabasz_score(x, labels)
