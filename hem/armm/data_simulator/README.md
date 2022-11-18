# Generating Simulated Data

Simulated data facilitated the creation of the ARMM framework. It was integral to build algorithms to cluster non-fungible tokens' attributes. Furthermore, unit tests and integrations tests motivated its creation. User assumes risk using these simulated data to build new clustering and pricing models as it is not real market data. Non-heuristic models should be trained with real market data.

## main.py

```
    :param n: number of simulated data to generate
    :param missing_allowed: whether it is allowed to have missing data in simulation
```

## Attribute definitions/types

The implementation follows the `names` and `types` of attributes defined in [Table of Token Attributes](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/data-model-ingestion.md#table-of-token-attributes) and
[initial test data for Ingest process](https://docs.google.com/spreadsheets/d/1A_cYJFvlUrDLyqUoaXckB2UPW_sFLKMiDXxLJsiQtYM/edit#gid=0)

Following is a summary of distributions used in generating data:
1. `num_owners`: Poisson with mean=1
2. `num_price_chg`: Poisson with mean=1
3. `nft_age`: Poisson with mean=15
4. `avg_price`: Normal, mean specified based on minting country, project category, and project type, variance = 5
5. `last_price`: Normal, mean= `avg_price`, variance = 5
6. `country`: uniform [`BGR`, `ETH`, `FRA`, `GBR`, `GIN`, `GTM`, `HND`, `IDN`, `IND`,
                        `KEN`, `KHM`, `MMR`, `MOZ`, `NIC`, `PER`, `RWA`, `USA`]
7. `project_category`: uniform [`WASTE_MGMT`, `RENEW_ENERGY`,
                                 `FOREST_CONSERV`, `COMM_ENRGY_EFF`]
8. `project_type`: selected from a pool based on `project_category`
   1. `WASTE_MGMT`:  `EMM_RED`
   2. `RENEW_ENERGY`: uniform [`SOLAR`, `WIND`, `HYDRO`]
   3. `FOREST_CONSERV`: `AGG_LAND_MGMT`
   4. `COMM_ENRGY_EFF`: uniform [`COOK_STV`, `WATER`, `BIOGAS`]
9. if `missing_allowed == True`, 50% of data with `num_owners == 1` have missing price information


### Future Considerations

1. Currently prices are broken up by country. It may be worthwhile to account for geospatially correlated prices, i.e. countries closer together
will have similar prices than those farther apart. Instead of conditioning on the country name, use a [spatial function](https://pdixon.stat.iastate.edu/stat406/notes/part%209%20sim%20annotated.pdf)
2. List of countries is the same for setting different means in price. It will be worthwhile to have different lists to be able to validate that
the grid search algorithm to determine optimal number of k is reasonable and number of categories can influence this.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
