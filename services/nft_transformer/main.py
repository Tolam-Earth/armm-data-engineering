from typing import List

from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError

from hem.armm import nft, geo, handlers

app = FastAPI()
# apply handler to our app. A little different from docs with @app.exception_handler()
# wrapping a def fxn() so we can re-use common handlers across fastapi apps
app.exception_handler(RequestValidationError)(handlers.validation_exception_handler)
API_PREFIX = '/arm/v1'

geocoder = geo.GeoCoder()


@app.get('/')
async def root():
    return {'message': f'Use {API_PREFIX}'}


@app.get(API_PREFIX)
async def prefix():
    return {'message': API_PREFIX}


@app.post(f'{API_PREFIX}/data_transformer', response_model=nft.NftTransformedResponse)
def nft_transform(details: List[nft.NftDetails]):
    transformed = [nft.transform_details(x, geocoder) for x in details]
    return nft.records_to_list(transformed)
