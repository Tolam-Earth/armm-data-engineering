# Pricing model

## Model

The pricing model is based on the [ARM Pseudo-Code](https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA). To use the pricing
model, the following steps are necessary:

1. NFTs in the current seed data should be labeled using clustering
   algorithm ([Pooling Classifier API](api_pooling_classifier.md))
2. [Table of Pool](../data-model-ingestion.md#table-of-pool-summaries) should be defined for all the pools based on the
   seed data and
   their labels. Pricing API will use these tables to define the $X$ and $Q$ matrices used
   in [ARM Pseudo-Code](https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA).
3. The incoming NFTs for pricing must be labeled using the clustering
   model ([Pooling Classifier API](api_pooling_classifier.md))
4. NFTs with the same label should form a request to ARMM. For each request to ARMM, Pricing API will define $\Delta q$
   used in [ARM Pseudo-Code](https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA)

Based on the [Input Parameters](pricing-api.md#input-parameters), Pricing API will define the minimum recommended price
as the maximum price that [ARMM](https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA) is willing to pay for buying the NFTs,
and the maximum recommended price as the minimum price that [ARMM](https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA) is willing
to receive for selling the NFTs.

## Implementation

The `main.py` imports two underlying functions stored in `pricing.py`. These functions are the python implementation of
the [ARM Pseudo-Code](https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA).
Particularly, `arm_buys_price` returns the max price that ARMM is willing to buy the NFTs for, and `arm_sells_price`
returns the min price that ARMM is willing to sell the NFTs for. The `main` function returns these prices respectively
as the minimum and maximum recommended prices.

Additionally, `pricing.py` contains `eigenvalues_calculator` function that requires $X$ and $Q$ or $Q + \Delta q$ as
inputs, and returns the eigenvalues of $XQX^T$ or $X(Q + Δq)X^T$.

## Inputs and outputs

```
    :param pool_id: pool id of NFTs to be priced
    :param n_nft: number of NFTs in the current call
    :param pool_meta: the metadata of all pools
    :param r: quantity of a reserve currency in USD cents

    :return: dictionary with min and max recommended prices
```


### Python Sample Run
```
cd <your-path>/hem-armm-engineering/hem/armm/pricing
python ./main.py cc251a50-a1ac-4ddc-92a8-2bdb57df29ab 20 ../clusterin/data/pool_meta.json 10000000
```
this code calculates the price per nft for the `20` NFTs from pool `cc251a50-a1ac-4ddc-92a8-2bdb57df29ab` 
using the pool meta `hem-armm-engineering/hem/armm/clustering/data/pool_meta.json` with the assumption of having `10000000` USD cents reserves, and saves a 
json file with the minimum and maximum recommended prices. 

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at: 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
