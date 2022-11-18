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
cd <your-path>/hem-armm-engineering
python ./hem/armm/clustering/predict/main.py ./services/nft_classifier/model.pkl ./hem/armm/clustering/data/simulated_data.csv
```
this code runs the `main.py` to assign labels to the data points in `hem-armm-engineering/hem/armm/clustering/data/simulated_data.csv`
using the pretrained model stored in `hem-armm-engineering/services/nft_classifier/model.pkl`.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
