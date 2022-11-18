# NFT Classifier Service

This is a RESTful microservice that classifies an [NFT](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/api_pooling_classifier.md#request-body)
to an [NFT pool](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/api_pooling_classifier.md#response).
It is deployed within the [dataflow to ingest NFT Detail data](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/ARMM-ingest-nft-data.md).

## Sample HTTP request
```bash
curl -X POST http://127.0.0.1:8001/arm/v1/classification/scheduled_pool \
  -H "Content-Type: application/json" \
  --data-binary @- <<EOF
  { "nft_id": [{"token_id": "0.0.9401", "serial_number": 1}], 
    "transaction_id": ["0.0.9401@1602138343.335616988"], 
    "transaction_time": [{"seconds": 1566015267, "nanos": 0}], 
    "minting_owner": ["0.0.9401"], 
    "owner": ["0.0.9401"], 
    "country": ["CHN"], 
    "first_subdivision": ["GD"], 
    "latitude": [23.1357694], 
    "longitude": [113.1982688], 
    "project_category": ["RENEW_ENERGY"], 
    "project_type": ["SOLAR"], 
    "vintage_year": [2020], 
    "nft_age": [2], 
    "num_owners": [1], 
    "avg_price": [0], 
    "last_price": [10000], 
    "num_price_chg": [2], 
    "nft_state": ["LISTED"]
  }
EOF
```

which returns:

```json
{ "nft_id":["0.0.9401.1"],
  "transaction_id":["0.0.9401@1602138343.335616988"],
  "transaction_time":[1566015267000000000],
  "token_pool_id":["272986af-24ea-4473-a4a3-99acb70128c5"],
  "name_pool":["GTM_KHM_KEN_BGR_GBR_IND_IDN_PER_RWA_FRA_HND_ETH_NIC_MMR_GIN_MOZ_USA_RENEW_ENERGY_SOLAR_272986af-24ea-4473-a4a3-99acb70128c5"],
  "pooling_version":["0.0.0.0"]
}
```

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
