from typing import List, Optional
from pydantic import BaseModel, validator
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

import hem.armm.pricing.main
from hem.armm import handlers, nft

API_PREFIX = '/arm/v1'
PRICING = 'price-range'
MIN_NFTS_TO_PRICE = 1
MAX_NFTS_TO_PRICE = 600

app = FastAPI()
app.exception_handler(RequestValidationError)(handlers.validation_exception_handler)


class PricingRequest(BaseModel):
    """
    https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/pricing-api.md#request-body
    """
    endpoint_id: Optional[int] = 0  # Not needed yet. Model is imported for now.
    pool_id: str
    n_nft: int
    pools: List[nft.PoolMeta]

    @validator('n_nft')
    def n_nft_range(cls, v):
        if v < MIN_NFTS_TO_PRICE or v > MAX_NFTS_TO_PRICE:
            raise ValueError(
                f"n_nft={v} is outside the valid range of [{MIN_NFTS_TO_PRICE}, {MAX_NFTS_TO_PRICE}]."
            )
        return v

    @validator('pools')
    def empty_pools(cls, v):
        if len(v) < 1:
            raise ValueError(
                f"Empty list of 'pools' is invalid. The list must have at least one element."
            )
        return v


class PricingResponse(BaseModel):
    """
    https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/pricing-api.md#response
    """
    min_price_usd_cents: int
    max_price_usd_cents: int


@app.get('/')
async def root():
    return {'message': f'POST requests to: {API_PREFIX}/{PRICING}'}


@app.get(API_PREFIX)
async def prefix():
    return {'message': f'POST requests to: {API_PREFIX}/{PRICING}'}


@app.post(f'{API_PREFIX}/{PRICING}', response_model=PricingResponse)
def price_range(pricing_request: PricingRequest) -> PricingResponse:
    pools = [pool.dict() for pool in pricing_request.pools]
    price_interval = hem.armm.pricing.main.main(
        pricing_request.pool_id,
        pricing_request.n_nft,
        pools
    )
    response = PricingResponse(
        min_price_usd_cents=price_interval['min_price_usd_cents'],
        max_price_usd_cents=price_interval['max_price_usd_cents']
    )
    return response
