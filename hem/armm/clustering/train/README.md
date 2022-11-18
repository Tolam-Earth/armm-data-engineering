# Clustering model training

## Inputs and outputs

```
    :param data_address: the address to the .csv file containing the training data
    :param n_splits: number of folds for k-fold cross-validation
    :param n_init: number of times the clustering algorithm will be run with different centroid initialization
    :param n_jobs: number of jobs to run in parallel with gridsearch algorithm
    :param pooling_version: a str to be recorded as the model's version
```
This main.py file optimizes the number of clusters using gridsearch. As output, saves
`model.pkl`: the trained pipeline (preprocessor and clustering model).

### Python Sample Run
```
cd <your-path>/hem-armm-engineering/hem/armm/clustering/train
python ./main.py ../data/simulated_data.csv 5 1 -1 0.0.0.0
```
this code runs the main.py on `hem-armm-engineering/hem/armm/clustering/data/simulated_data.csv` using `n_splits=5` `n_init=1` `n_jobs=-1` and recoding the `pooling_version` as `0.0.0.0`.
Optimization is performed using  5-fold cross-validation (`n_splits=5`) and using all available cpus for parallelization (`n_jobs=-1`). 

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
