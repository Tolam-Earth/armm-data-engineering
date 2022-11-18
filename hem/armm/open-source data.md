# Open-source simulated data

## Usage

The simulated data was used for the training of the clustering model and the definition of pool metadata.

## Details

The simulated data includes 5,000 rows with randomly created attribute values as follows
* `project_category`: randomly selected from `['WASTE_MGMT', 'RENEW_ENERGY',
                                 'FOREST_CONSERV', 'COMM_ENRGY_EFF']`
* `project_type`: selected from a list based on `project_category`
   1. `project_category` == `WASTE_MGMT`:  `EMM_RED`
   2. `project_category` == `RENEW_ENERGY`: randomly selected from `['SOLAR', 'WIND', 'HYDRO']`
   3. `project_category` == `FOREST_CONSERV`: `AGG_LAND_MGMT`
   4. `project_category` == `COMM_ENRGY_EFF`: randomly selected from `['COOK_STV', 'WATER', 'BIOGAS']`
* `country`: randomly selected from [`BGR`, `ETH`, `FRA`, `GBR`, `GIN`, `GTM`, `HND`, `IDN`, `IND`,
                        `KEN`, `KHM`, `MMR`, `MOZ`, `NIC`, `PER`, `RWA`, `USA`]
* GPS Coordinates (`longitude` and `latitude`): computed based on the selected `country`
* Age of NFT (`nft_age`): randomly selected from a Poisson distribution with mean = 15
* Number of Previous Owners (`num_owners`): randomly selected from a Poisson distribution with mean = 1
* Number of Price Changes (`num_price_chg`): randomly selected from a Poisson distribution with mean = 1
* Average Price (`avg_price`): randomly selected from a Normal distribution with mean specified based on project Category and country, and variance=5
* Last Price (`last_price`): randomly selected from a Normal distribution with mean= `avg_price`, variance = 5

## Location

The simulated data is stored in `./clustering/data/simulated_data.csv`.

## Notes
1. For this specific simulation, the optimal number of clusters was defined to be equal to the number of project types.
2. Simulated data is used for MVP.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.