
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

import uuid
from numpy import random

from hem.armm.data_simulator.test_cases_json.underlying.NFTClass import NFTClass
from hem.armm.data_simulator.test_cases_json.underlying.helper import COUNTRY_FIRST_SUBDIVISION_DICT, PROJECT_CAT_LIST, \
    GPS_COORDINATES, define_project_type

NUM_OWNER = 10
NUM_NFT = 100
MIN_NUM_SAME_NFT = 1
MAX_NUM_SAME_NFT = 2
MIN_TRANSACTION_SECONDS = 1_500_000_000
MAX_TRANSACTION_SECONDS = 1_700_000_000
MIN_TRANSACTION_NANO = 100_000_000
MAX_TRANSACTION_NANO = 999_999_999
MIN_VINTAGE_YEAR = 2015
MAX_VINTAGE_YEAR = 2022


def create_minted(n_simulations):
    """

    Parameters
    ----------
    n_simulations: total number of nfts to be created

    Returns
    -------
    list of the MINTED nft classes with length=n_simulations

    """
    random_ids = random.choice(range(10_000_000, 100_000_000), size=[NUM_OWNER + NUM_NFT], replace=False)
    universe_of_owner = random_ids[:NUM_OWNER]
    universe_of_nft_id = random_ids[NUM_OWNER:]
    minted_items = []
    for idx, nft in enumerate(universe_of_nft_id):
        random_owner = random.choice(universe_of_owner)
        if n_simulations <= MIN_NUM_SAME_NFT or nft == universe_of_nft_id[-1]:
            num_nfts = n_simulations
        else:
            num_nfts = random.randint(MIN_NUM_SAME_NFT, min(MAX_NUM_SAME_NFT, n_simulations))
        n_simulations -= num_nfts
        token_id = f"0.0.{nft}"
        minting_owner = f"0.0.{random_owner}"
        transaction_time_seconds = random.randint(MIN_TRANSACTION_SECONDS, MAX_TRANSACTION_SECONDS)
        transaction_time_nano = random.randint(MIN_TRANSACTION_NANO, MAX_TRANSACTION_NANO)
        transaction_id = f"{minting_owner}-{transaction_time_seconds}-{transaction_time_nano}"
        country = random.choice(list(COUNTRY_FIRST_SUBDIVISION_DICT.keys()))
        first_subdivision = random.choice(COUNTRY_FIRST_SUBDIVISION_DICT[country])
        latitude, longitude = GPS_COORDINATES[country][first_subdivision]
        project_category = random.choice(PROJECT_CAT_LIST)
        project_type = define_project_type(project_category)
        vintage_year = random.randint(MIN_VINTAGE_YEAR, MAX_VINTAGE_YEAR)
        device_id = str(uuid.uuid4())
        guardian_id = str(uuid.uuid4())

        for serial_number in range(1, num_nfts + 1):
            serial_number = str(serial_number)
            minted_items.append(NFTClass(token_id=token_id,
                                         serial_number=serial_number,
                                         transaction_id=transaction_id,
                                         transaction_time_seconds=transaction_time_seconds,
                                         transaction_time_nano=transaction_time_nano,
                                         minting_owner=minting_owner,
                                         country=country,
                                         first_subdivision=first_subdivision,
                                         latitude=latitude,
                                         longitude=longitude,
                                         project_category=project_category,
                                         project_type=project_type,
                                         vintage_year=vintage_year,
                                         device_id=device_id,
                                         guardian_id=guardian_id,
                                         ))
        if n_simulations == 0:
            break
    return minted_items


def create_nft_details_schema(nft):
    """

    Parameters
    ----------
    nft: the MINTED nft

    Returns
    -------
    a dictionary (json) as the input received for ingestion for each nft

    """
    return {"msg_type": nft.nft_state[0],
            "nft_id": nft.nft_id,
            "minting_owner": nft.minting_owner,
            "minting_time": nft.transaction_time[0],
            "vintage_year": nft.vintage_year,
            "transaction_id": nft.transaction_id[0],
            "transaction_memo": nft.transaction_memo,
            "project_category": nft.project_category,
            "project_type": nft.project_type,
            "country": nft.country,
            "first_subdivision": nft.first_subdivision,
            "device_id": nft.device_id,
            "guardian_id": nft.guardian_id,
            }
