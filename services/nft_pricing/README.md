# NFT Pricing Service

This is a RESTful microservice that estimates a [price range](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/pricing-api.md#response)
for a [set of NFTs in a pool](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/pricing-api.md#request-body).
It is deployed within the [pricing dataflow](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/ARMM-pricing-request.md).

The `request-100-nft.json` file used in the sample request below is a JSON request to price 100 NFTs.
Note that the full set of [pool_meta](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/data-model-ingestion.md#table-of-pool-summaries) data must be submitted in each request. 

## Sample HTTP request
```bash
# Assumes you run this command from the root directory of the project.
cd <your-path>/hem-armm-engineering
curl -X POST http://127.0.0.1:8002/arm/v1/price-range \
  -H "Content-Type: application/json" \
  --data-binary @- < tests/nft_pricing/data/request-100-nft.json
```

which returns:

```json
{ "min_price_usd_cents": 190690,
  "max_price_usd_cents": 220151
}
```
