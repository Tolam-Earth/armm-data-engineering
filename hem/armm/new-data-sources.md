# Change/Add New Data sources

The data sources and models in the current ARMM implementation are static and hard-coded, and therefore, there are no 
codes in place that facilitate changing and/or adding new data sources. However, if the new data follows the same 
headers and formats of the original data, customized data sources can be used in two different levels

1. [Training new clustering model](#training-new-clustering-model) 
2. [Defining new pool metadata](#defining-new-pool-metadata)


## Training new clustering model 

In the ARMM implementation, data sources are employed in the definition of the clustering model
([Clustering model](./clustering/train/README.md))
and the pool metadata ([Creating pool_meta tables](./clustering/pool_meta/README.md)).
Utilizing a new clustering model reflects a major update in the ARMM, which can be done by the following steps:

1. Define the new data with the same format as our simulated data stored
at `hem-armm-engineering/hem/armm/clustering/data/simulated_data.csv`.
2. Following [Clustering model](./clustering/train/README.md),
train a new clustering model that will be stored as `model.pkl`.
3. Following [Clustering the test data](./clustering/predict/README.md),
use the trained model to define the labels of the data points.
4. Following [Creating pool_meta tables](./clustering/pool_meta/README.md),
use the trained model and the labeled data to create the `pool_meta.json`.
5. You can now update ARMM by using the new `model.pkl` and `pool_meta.json`.


## Defining new pool metadata 

It is possible to just customize the `pool_meta.json` without retraining the clustering model. To do so, the following steps 
can be taken:

1. Define the new data with the same format as our simulated data stored
at `hem-armm-engineering/hem/armm/clustering/data/simulated_data.csv`.
2. Following [Clustering the test data](./clustering/predict/README.md),
use a trained model to define the labels of the new data points.
3. Following [Creating pool_meta tables](./clustering/pool_meta/README.md),
use the trained model and the labeled data to create the `pool_meta.json`.
4. You can now update ARMM by using the new `pool_meta.json`.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.