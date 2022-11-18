# Underlying modules for clustering model

## basemodel.py

contains the template of the class of clustering model(currently BisectingKMeans). The class has modified `score` function to return 
the pseudo F statistic (`calinski_harabasz_score`) as the metric for the goodness of clustering.

## basemodel_GM_templated.py

contains the current class of clustering model (GaussianMixture). The child class has modified `score` function to return 
the pseudo F statistic as the metric for the goodness of clustering.

## pipelinemodel.py

contains the function that creates the pipeline using the preprocessing and the clustering model.

The input is defined as dict keywords because different clustering models might have different names for number of clusters.
As example, BisectingKMeans calls number of clusters `n_clusters` while GaussianMixture calls them `n_components`.


## gridsearch.py

contains the function to perform gridsearch optimization over the `n_clusters`.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
