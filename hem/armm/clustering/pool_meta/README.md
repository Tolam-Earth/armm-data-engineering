# Creating pool_meta tables

## Inputs and outputs

```
    :param model: the trained clustering model
    :param data: the pandas DataFrame containing the labeled data
    :param dt_pool: an integer showing a user-defined date-time point
```

This `main.py` and `main` functions uses a previously trained model in `model` and the dataframe of the labeled data
points to create the token pool metadata (`pool_meta`) as specified in
[Table of Pool Summaries](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/data-model-ingestion.md#table-of-pool-summaries)
. As output, saves
a single file `pool_meta.json`, the JSON file of the token pool metadata tables.

### Python Sample Run

```
cd <your-path>/hem-armm-engineering
python ./hem/armm/clustering/pool_meta/main.py ./services/nft_classifier/model.pkl ./hem/armm/clustering/data/clustered-data.csv 0
```

this code runs the `main.py` to create and save token pool metadata tables using the pretrained model stored in `hem-armm-engineering/services/nft_classifier/model.pkl`
and the labeled data points in `hem-armm-engineering/hem/armm/clustering/data/clustered-data.csv`.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
