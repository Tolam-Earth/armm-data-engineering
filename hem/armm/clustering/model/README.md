# Underlying modules for clustering model

## basemodel.py

contains the child class of the parent clustering model(currently BisectingKMeans). The child class has modified `score` function to return 
the pseudo F statistic (`calinski_harabasz_score`) as the metric for the goodness of clustering.

## basemodel_GM_templated.py

contains the template of how to have a different parent clustering model (GaussianMixture). The child class has modified `score` function to return 
the pseudo F statistic as the metric for the goodness of clustering.

To use, simply rename to `basemodel.py`.

## pipelinemodel.py

contains the function that creates the pipeline using the preprocessing and the clustering model.

The input is defined as dict keywords because different clustering models might have different names for number of clusters.
As example, BisectingKMeans calls number of clusters `n_clusters` while GaussianMixture calls them `n_components`.


## gridsearch.py

contains the function to perform gridsearch optimization over the `n_clusters`.
