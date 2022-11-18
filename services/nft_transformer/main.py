
# Copyright (c) 2022 Tolam Earth
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

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
