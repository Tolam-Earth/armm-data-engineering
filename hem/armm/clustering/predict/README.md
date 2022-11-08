# Clustering the test data

## Inputs and outputs

```
    :param model_address: location of trained pipeline
    :param data_address: location of the test dataset as .csv file
```
This main.py file assigns `token_pool_id` to the input data. As output, saves
a single file.

1. 'clustered-data.csv': the csv file based on the input data with an additional column `token_pool_id`

### Python Sample Run
```
python ./main.py ./model.pkl ../data/test.csv
```
this code runs the main.py to assign labels to `../data/test.csv` using `model.pkl`.
