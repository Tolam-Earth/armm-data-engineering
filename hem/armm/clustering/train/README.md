# Clustering model training

## Inputs and outputs

```
    :param data_address: the address to the .csv file containing the training data
    :param n_splits: number of folds for k-fold cross-validation
    :param n_init: number of times the clustering algorithm will be run with different centroid initialization
    :param n_jobs: number of jobs to run in parallel with gridsearch algorithm
```
This main.py file optimizes the number of clusters using gridsearch. As output, saves
saves 'model.pkl': the trained pipeline (preprocessor and clustering model).

### Python Sample Run
```
python ./main.py ../data/train.csv 5 1 -1
```
this code runs the main.py on data/train.csv using `n_splits=5` `n_init=1` `n_jobs=-1`.
Optimization is performed using  5-fold cross-validation (`n_splits=5`) and using all available cpus for parallelization (`n_jobs=-1`). 
