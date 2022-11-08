# NFT Transformer Service

This is a RESTful microservice that transforms and augments [NFT Detail data](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/data-model.md#nft-details-table)
as needed for downstream machine learning applications. It is deployed within
the [dataflow to ingest NFT Detail data](https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/ARMM-ingest-nft-data.md).

**Contents**

- [Development environment](#development-environment)
- [Running the unit tests](#running-the-unit-tests)
- [Building a Docker image](#building-a-Docker-image)
    - [Running the Docker image](#running-the-docker-image)
    - [Sample HTTP request](#sample-http-request)
    - [Sample error messages](#sample-error-messages)
- [Running the service locally](#running-the-service-locally)
    - [Sample HTTP request](#sample-http-request)
- [Viewing the API](#viewing-the-api)
---

## Development environment
This service is implemented in [Python](https://www.python.org/),
using the [FastAPI framework](https://fastapi.tiangolo.com/).
It is built as a [Docker](https://www.docker.com/) image to be deployed
to Google [Cloud Run](https://cloud.google.com/run).
As a web service, it accepts JSON in the request body and returns JSON in
the response body.

See [pyproject.toml](../../pyproject.toml) and the [project-level README](../../README.md) for more details about the development environment.

## Running the unit tests
```bash
cd <your-path>/hem-armm-engineering
python -m pytest
```

## Building a Docker image
```bash
cd <your-path>/hem-armm-engineering
docker build -f services/nft_transformer/Dockerfile -t nft-transformer .
```

### Running the Docker image
```bash
# --rm removes the container automatically when it stops running.
# --publish 8000:8080 exposes FastAPI's port 8080 in container as port 8000 on local machine.
docker run --rm --publish 8000:8080 --interactive --tty --workdir /app --name nft-transformer nft-transformer
```

### Sample HTTP request
```bash
curl -X POST http://127.0.0.1:8000/arm/v1/data_transformer \
  -H "Content-Type: application/json" \
  --data-binary @- << EOF
[ { "nft_id": {"token_id": "1.2.3", "serial_number": 1}, 
    "msg_type": ["MINTED", "LISTED", "PURCHASED", "LISTED"], 
    "country": "CHN", 
    "first_subdivision": "GD", 
    "minting_time": 1661141001, 
    "transaction_id": [
      "abc12345678", 
      "abc23456791", 
      "abc34568012",
      "abc45680123"
    ], 
    "transaction_time": [
      {"seconds": 1661967010, "nanos": 335616988}, 
      {"seconds": 1661967145, "nanos": 335616980}, 
      {"seconds": 1661967300, "nanos": 335616989},
      {"seconds": 1662071002, "nanos": 335616989}
    ], 
    "owner": ["0.0.45", "0.0.45", "0.0.90", "0.0.90"], 
    "price": [0, 4522, 4500, 6090]
  }
]
EOF
```

which returns:

```json
{ "nft_id":[{"token_id":"1.2.3", "serial_number":1}],
  "current_owner":["0.0.90"],
  "nft_age":[10],
  "num_owners":[2],
  "avg_price":[4500.0],
  "last_price":[4500],
  "num_price_chg":[2],
  "nft_state":["LISTED"],
  "latitude":[22.879047785500063],
  "longitude":[112.30351615339782]
}
```

Although the `nft_age` (in days) will be different when you run this request,
because the age is calculated with respect to the current time at the
time of the request.

### Sample error messages
This request has a `minting_time` value that exceeds the maximum
allowed value:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"minting_time": 253402300799123456789}' \
  http://127.0.0.1:8000/nft-transformer/v1/nft/details
```

It returns:

```json
{
  "request_body": {
    "minting_time": 253402300799123456789
  },
  "errors": [
    {
      "loc": [
        "body",
        "minting_time"
      ],
      "msg": "minting_time=253402300799123456789 as integer nanoseconds from Unix epoch is not in the expected range [-2177452800000000000, 253402300799000000000] = [0001-01-01T00:00:00Z, 9999-12-31T23:59:59Z].",
      "type": "value_error"
    }
  ],
  "nft_age": null
}
```

Another example has a malformed `asset_id`:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"asset_id": "0.0.1", "minting_time": 1566015267000000000}' \
  http://127.0.0.1:8000/nft-transformer/v1/nft/details
```

which returns:

```json
{
  "request_body": {
    "asset_id": "0.0.1",
    "minting_time": 1566015267000000000
  },
  "errors": [
    {
      "loc": [
        "body",
        "asset_id"
      ],
      "msg": "asset_id='0.0.1' is not formatted with four components as shard.realm.num.serialnumber",
      "type": "value_error"
    }
  ],
  "nft_age": null
}
```

## Running the service locally
The server does _not_ need to be running, in order to run unit tests. However,
if you want to submit HTTP requests to the service while developing locally,
start the service locally with this command:

```bash
cd <your-path>/hem-armm-engineering/services/nft_transformer
uvicorn main:app --reload
```

Use `<CTRL-C>` to stop the service.

### Sample HTTP request
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"minting_time": 1566015267000000000}' \
  http://127.0.0.1:8000/nft-transformer/v1/nft/details
```

which returns:

```json
{"nft_age":1103,"errors":null}
```

Although the `nft_age` (in days) will be different when you run this request,
because the age is calculated with respect to the current time at the
time of the request.

## Viewing the API
The API documentation is available at:

```
http://<domain>:<port>/docs
```

For example:
```
http://127.0.0.1:8000/docs
```
