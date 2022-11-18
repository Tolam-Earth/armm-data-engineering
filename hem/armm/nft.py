
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

import time
from typing import Optional, List, Dict
from enum import Enum

import numpy as np
from pydantic import BaseModel, validator, Field, constr, root_validator

from hem.armm.geo import GeoCoder

SECONDS_PER_DAY = 86400.0
NANOSECONDS_PER_SECOND = 10**9
NANOSECONDS_PER_DAY = SECONDS_PER_DAY * NANOSECONDS_PER_SECOND

# Valid integer range for a Hedera Timestamp, according to:
# https://docs.hedera.com/guides/docs/hedera-api/miscellaneous/timestamp and
# https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/timestamp.proto
MIN_NANOSECONDS_FROM_UNIX_EPOCH = -2177452800000000000   # 0001-01-01T00:00:00Z
MAX_NANOSECONDS_FROM_UNIX_EPOCH = 253402300799000000000  # 9999-12-31T23:59:59Z


class NftId(BaseModel):
    token_id: str = Field(..., regex=r"^\d+\.\d+\.\d+$", description="Hedera token ID in the form of shard.realm.num")
    serial_number: int = Field(..., ge=0)  # serial_number is a positive integer


class TransactionTime(BaseModel):
    seconds: int = Field(..., ge=0, description="Seconds since the epoch")
    nanos: int = Field(0, ge=0, description="nanoseconds since the last second")


class MessageType(str, Enum):
    """
    Message Types for NFTs
    https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/token_marketplace_state_topic.md
    """
    MINTED = "MINTED"
    LISTED = "LISTED"
    PURCHASED = "PURCHASED"
    UNLISTED = "UNLISTED"
    RETRACTED = "RETRACTED"
    RETIRED = "RETIRED"


class NftDetails(BaseModel):
    nft_id: NftId
    # country: ISO 3166 Alpha-3 country code standard e.g. USA
    country: constr(to_upper=True, regex=r"^[A-Z]{3}$")
    # first_subdivision: The two-letter code element from ISO 3166-1. e.g. Missouri, USA is MO
    first_subdivision: constr(to_upper=True, regex=r"^[A-Z0-9]{2,3}$")
    msg_type: List[MessageType]
    transaction_id: List[str]
    transaction_time: List[TransactionTime]
    owner: List[str] = Field(..., regex=r"^\d+\.\d+\.\d+$",
                             description="Hedera token ID in the form of shard.realm.num")
    price: List[Optional[int]] = Field(..., ge=0, description="Price in USD cents")

    @property
    def market_age(self) -> int:
        """
        :return: int (current time - first transaction time) in days
        """
        min_transaction_time = min(self.transaction_time, key=lambda x: (x.seconds * NANOSECONDS_PER_SECOND) + x.nanos)
        min_transaction_time_ns = (min_transaction_time.seconds * NANOSECONDS_PER_SECOND) + min_transaction_time.nanos
        now_epoch_ns = time.time_ns()
        market_age = int((now_epoch_ns - min_transaction_time_ns) / NANOSECONDS_PER_DAY)
        return market_age

    @root_validator()
    def validate_same_length(cls, field_values):
        list_fields = ['msg_type', 'transaction_id', 'transaction_time', 'owner', 'price']
        list_values = [v for k, v in field_values.items() if k in list_fields]
        # use an iterator, so we only calculate length once per item
        it = iter(list_values)
        first_length = len(next(it))
        if any(len(val) != first_length for val in it):
            raise ValueError('Lists must all be the same length!')
        return field_values


class NftMintedResponse(BaseModel):
    """ @returns derived values only. """
    nft_age: Optional[int] = None
    errors: Optional[list] = None  # List of error objects


class NftTransformedResponse(BaseModel):
    nft_id: List[NftId]
    current_owner: List[str] = Field(..., regex=r"^\d+\.\d+\.\d+$",
                                     description="Hedera token ID in the form of shard.realm.num")
    nft_age: List[int] = Field(..., ge=0, description='Number of days that NFT has been listed on the market')
    num_owners: List[int] = Field(..., ge=1)
    avg_price: List[float]
    last_price: List[int]
    num_price_chg: List[int]
    nft_state: List[MessageType]
    latitude: List[Optional[float]]
    longitude: List[Optional[float]]

    @root_validator()
    def validate_same_length(cls, field_values):
        # use an iterator, so we only calculate length once per item
        it = iter(field_values.values())
        first_length = len(next(it))
        if any(len(val) != first_length for val in it):
            raise ValueError('Lists must all be the same length!')
        return field_values


def transform_details(nft_details: NftDetails, geocoder: GeoCoder):
    """
    Transforms NftDetails into properties used for modeling
    :param nft_details: NftDetails object
    :type nft_details: NftDetails
    :param geocoder: GeoCoder object to use geocoder.geocode()
    :type geocoder: GeoCoder
    :return: Dictionary of properties to pass to records_to_list and then populate NftTransformedResponse
    :rtype: Dict[str, any]
    """
    # get the latest transaction time and its index
    latest_transaction_time = max(nft_details.transaction_time, key=lambda x: x.seconds)
    latest_transaction_index = nft_details.transaction_time.index(latest_transaction_time)

    # geocode country-subdivision
    longitude, latitude = geocoder.geocode(nft_details.country,
                                           nft_details.first_subdivision)

    # average and last calculated only from PURCHASED prices.
    purchased_prices = [
        price for (price, msg_type)
        in zip(nft_details.price, nft_details.msg_type)
        if price is not None and msg_type is MessageType.PURCHASED
    ]
    avg_price = int(np.nanmean(purchased_prices)) if len(purchased_prices) > 0 else 0
    last_price = purchased_prices[-1] if len(purchased_prices) > 0 else 0

    num_owners = len(np.unique(nft_details.owner))

    # num_price_chg: Pairwise comparison of LISTED and PURCHASED sequence of prices.
    price_events = [
        price for (price, msg_type)
        in zip(nft_details.price, nft_details.msg_type)
        if price is not None and price != 0 and msg_type in [MessageType.LISTED, MessageType.PURCHASED]
    ]
    num_price_chg = 0
    if len(price_events) > 1:
        for i in range(0, len(price_events) - 1):
            if price_events[i] != price_events[i + 1]:
                num_price_chg += 1

    current_owner = nft_details.owner[latest_transaction_index]
    nft_state = nft_details.msg_type[latest_transaction_index]

    return {
        "nft_id": nft_details.nft_id,
        "current_owner": current_owner,
        "nft_age": nft_details.market_age,
        "num_owners": num_owners,
        "avg_price": avg_price,
        "last_price": last_price,
        "num_price_chg": num_price_chg,
        "nft_state": nft_state,
        "latitude": latitude,
        "longitude": longitude,
    }


def records_to_list(records: List[Dict]) -> Dict:
    """Convert a list of records into a dictionary with each key being a list of the values"""
    # assume uniform records or at least the first record has keys in common with the rest
    keys = records[0].keys()
    return {
        k: [record[k] for record in records]
        for k in keys
    }


class PoolMeta(BaseModel):
    version_pool: str
    dt_pool: int
    id: str
    name_pool: str
    attributes_pool: List[str]
    category_pool: List[str]
    mean_pool: List[float]
    median_pool: List[float]
    var_pool: List[float]
    stdev_pool: List[float]
    n_pool: int
