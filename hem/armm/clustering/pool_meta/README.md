# Clustering the test data

## Inputs and outputs

```
    :param model: the address to the trained pipeline
    :param data: the address to the csv file containing the data
```
This main.py file uses the previously trained pipeline in `model_address` to assign `token_pool_id` to the input data, 
and using the same data and pipeline creates the token pool metadata (`pool_meta`) as specified in 
[Table of Pool Summaries](https://github.com/objectcomputing/hem-architecture/blob/harm-83/armm/information/data-model-ingestion.md#table-of-pool-summaries). As output, saves
two files

1. `clustered_data.csv`: the csv file based on the input data with an additional column `token_pool_id`
2. `pool_meta.json`: the JSON file of the token pool metadata table

### Python Sample Run
```
python ./main.py ./model.pkl ../data/train.csv
```
this code runs the main.py to assign clusters to `../data/train.csv` using `model.pkl`, and to create the token pool metadata table.
