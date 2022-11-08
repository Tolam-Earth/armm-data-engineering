# End-to-end test cases (.json files)

The test cases are defined using the definitions in [hem-architecture/armm/information](https://github.com/objectcomputing/hem-architecture/tree/main/armm/information)
and are stored in the following subfolders:

    '1-ARMM Ingests Minted NFT Flow/1-minted',
    '1-ARMM Ingests Minted NFT Flow/2-transformer/input',
    '1-ARMM Ingests Minted NFT Flow/2-transformer/output',
    '1-ARMM Ingests Minted NFT Flow/3-pooling_classifier/input',
    '1-ARMM Ingests Minted NFT Flow/3-pooling_classifier/output',
    '1-ARMM Ingests Minted NFT Flow/4-token_details_db',

    '2-ARMM Pricing Workflow/1-nft_pool_meta/input',
    '2-ARMM Pricing Workflow/1-nft_pool_meta/output',
    '2-ARMM Pricing Workflow/2-pricing/input',
    '2-ARMM Pricing Workflow/2-pricing/output',
    '2-ARMM Pricing Workflow/3-pricing_db',

    '3-ARMM Buy Agent Flow for MVP/1-marketplace_state',
    '3-ARMM Buy Agent Flow for MVP/2-query_ARMM/input',
    '3-ARMM Buy Agent Flow for MVP/2-query_ARMM/output',
    '3-ARMM Buy Agent Flow for MVP/3-buy_agent/input'

## 1-[ARMM Ingests Minted NFT Flow](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/ARMM-ingest-nft-data.md)


### 1-minted
A single JSON file with all the MINTED NFTs received for ingestion

### 2-transformer
Two JSON files stored at `/input` and `/output` containing the request and response body of 
[Transformer API](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/api_data_transformer.md)

### 3-pooling_classifier
Two JSON files stored at `/input` and `/output` containing the request and response body of 
[Pooling Classifier API](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/api_pooling_classifier.md)

### 4-token_details_db
A single JSON file with all NFTs' [Table of Token Attributes](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/data-model-ingestion.md#table-of-token-attributes)
to be written to the database



## 2-[ARMM Pricing Workflow](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/ARMM-pricing-request.md)

### 1-nft_pool_meta
A JSON file stored at `/input` with `nft_id` of NFTs in the pricing request

As the pricing requests are broken into NFTs with the same pool, 
JSON file stored at `/output` contains the `n` request body of
[Internal ARM Pricing APIs](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/pricing-api.md), where `n = # unique pools of the nfts in the current pricing request`.



### 2-pricing
JSON files stored at `/input` are the same as the outputs of `1-nft_pool_meta/output` 

JSON file stored at `/output` contains the `n` response body of
[Internal ARM Pricing APIs](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/pricing-api.md), where `n = # unique pools of the nfts in the current pricing request`.


### 3-pricing_db
A single JSON file with all NFTs' recommended prices to be written to the database

## 3-[ARMM Buy Agent Flow for MVP](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/ARMM-buy-agent-mvp.md)

### 1-marketplace_state
A single JSON file with LISTED NFTs
[NFT Token Marketplace State Message](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/token_marketplace_state_topic.md).

Note: For now, the listing price is randomly drawn from the uniform distribution of `[min_recommended price , max_recommended price + ( max_recommended - min_recommended)]`

### 2-query_ARMM
JSON file stored at `input` contains the `n=number of nfts`  input body of
[Internal Query to ARMM Databases](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/buy-agent-query.md) for each individual nft.

JSON file stored at `output` contains the `n=number of nfts`  Output body of
[Internal Query to ARMM Databases](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/buy-agent-query.md) for each individual nft.


### 3-buy_agent
JSON files stored at `input` contains the `n=number of nfts` 
[Buy Agent Token Message](https://github.com/objectcomputing/hem-architecture/blob/HARMM-138/armm/information/api/buy_agent_topic.md) for each individual nft.