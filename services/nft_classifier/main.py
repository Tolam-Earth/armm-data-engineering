from typing import List
import os
import pandas as pd
from pydantic import BaseModel, root_validator, validator
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from hem.armm.clustering.predict.main import main
from hem.armm import handlers, nft

API_PREFIX = '/arm/v1'
POOL = 'classification/scheduled_pool'

app = FastAPI()
app.exception_handler(RequestValidationError)(handlers.validation_exception_handler)


class ClassificationRequest(BaseModel):
    """
    Classification input model.
    See specification: https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/api_pooling_classifier.md#retrieve-user-information-endpoint
    Assumption: All Lists are the same length. For lists of length n,
        there are n NFTs represented. The value at position i for any
        list represents the value for nft[i].
    """
    nft_id: List[nft.NftId]
    transaction_id: List[str]
    transaction_time: List[nft.TransactionTime]
    minting_owner: List[str]
    owner: List[str]
    country: List[str]
    first_subdivision: List[str]
    latitude: List[float]
    longitude: List[float]
    project_category: List[str]
    project_type: List[str]
    vintage_year: List[int]
    nft_age: List[int]
    num_owners: List[int]
    avg_price: List[float]
    last_price: List[float]
    num_price_chg: List[int]
    nft_state: List[str]

    @validator('nft_id', allow_reuse=True)
    def has_non_empty_lists(cls, v):
        if len(v) < 1:
            raise ValueError(
                f"The input lists must hold at least one value each."
            )
        return v

    @root_validator()
    def validate_same_length(cls, field_values):
        list_fields = [
            'nft_id',
            'transaction_id',
            'transaction_time',
            'minting_owner',
            'owner',
            'country',
            'price',
            'first_subdivision',
            'latitude',
            'longitude',
            'project_category',
            'project_type',
            'vintage_year',
            'nft_age',
            'num_owners',
            'avg_price',
            'last_price',
            'num_price_chg',
            'nft_state']
        list_values = [v for k, v in field_values.items() if k in list_fields]
        # use an iterator, so we only calculate length once per item
        it = iter(list_values)
        first_length = len(next(it))
        if any(len(val) != first_length for val in it):
            raise ValueError('Input property lists must all be the same length!')
        return field_values


class ClassificationResponse(BaseModel):
    """
    See specification: https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/api_pooling_classifier.md#response
    """
    nft_id: List[nft.NftId]
    transaction_id: List[str]
    transaction_time: List[nft.TransactionTime]
    token_pool_id: List[str]
    name_pool: List[str]
    pooling_version: List[str]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "nft_age": None,
            "errors": exc.errors(),
            "request_body": exc.body
        }),
    )


@app.get('/')
async def root():
    return {'message': f'POST requests to: {API_PREFIX}/{POOL}'}


@app.get(API_PREFIX)
async def prefix():
    return {'message': f'POST requests to: {API_PREFIX}/{POOL}'}


@app.post(f'{API_PREFIX}/{POOL}', response_model=ClassificationResponse)
def classify(classification_request: ClassificationRequest):
    df = pd.DataFrame(classification_request.dict())
    prediction = main(
        os.path.join(os.path.dirname(__file__), 'model.pkl'),
        data=df
    )
    response = prediction.to_dict(orient='list')
    return response
