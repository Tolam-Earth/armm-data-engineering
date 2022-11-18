
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

import json
import os
import pytest
from fastapi.testclient import TestClient
from services.nft_pricing.main import app, API_PREFIX, PRICING

POOLS_JSON_RELATIVE_PATH = 'data/pool_meta.json'
EXPECTED_UNPROCESSABLE_ENTITY_CODE = 422
EXPECTED_UNPROCESSABLE_ENTITY_REASON = 'Unprocessable Entity'

client = TestClient(app)


@pytest.fixture
def pool_meta() -> list:
    """
    Loads a set of pools' data from a JSON file of the pool_meta table.
    :return: list representation of JSON data that defines pools.
    """
    full_json_file_path = os.path.join(os.path.dirname(__file__), POOLS_JSON_RELATIVE_PATH)
    with open(full_json_file_path) as pool_meta_json:
        pools = json.load(pool_meta_json)
    assert len(pools) > 1
    return pools


class TestNftClassifier:

    def test_single_nft(self, pool_meta):
        """
        Expects the price of a single NFT.
        :param pool_meta: fixture that loads pool_meta data.
        """
        response = client.post(
            f'{API_PREFIX}/{PRICING}',
            headers={"Content-Type": "application/json"},
            json={
                "endpoint_id": 0,  # Not implemented yet.
                "pool_id": "cc251a50-a1ac-4ddc-92a8-2bdb57df29ab",
                "n_nft": 1,
                "pools": pool_meta
            }
        )
        if response.status_code != 200:
            print(f"{response.content[0:500]=}")
        assert response.status_code == 200
        assert response.json()['min_price_usd_cents'] == 2037
        assert response.json()['max_price_usd_cents'] == 2040

    def test_many_nft(self, pool_meta):
        """
        Expects the total price of 100 NFTs from a single pool.
        :param pool_meta: fixture that loads pool_meta data.
        """
        response = client.post(
            f'{API_PREFIX}/{PRICING}',
            headers={"Content-Type": "application/json"},
            json={
                "endpoint_id": 0,  # Not implemented yet.
                "pool_id": "cc251a50-a1ac-4ddc-92a8-2bdb57df29ab",
                "n_nft": 100,
                "pools": pool_meta
            }
        )
        if response.status_code != 200:
            print(f"{response.content[0:500]=}")
        assert response.status_code == 200
        assert response.json()['min_price_usd_cents'] == 1906  # int(190690 / 100)
        assert response.json()['max_price_usd_cents'] == 2201  # int(220151 / 100)

    def test_empty_pools(self):
        """
        Expects a validation error, because pool_meta data is required.
        """
        response = client.post(
            f'{API_PREFIX}/{PRICING}',
            headers={"Content-Type": "application/json"},
            json={
                "endpoint_id": 0,
                "pool_id": "cc251a50-a1ac-4ddc-92a8-2bdb57df29ab",
                "n_nft": 1,
                "pools": []
            }
        )
        assert response.status_code == EXPECTED_UNPROCESSABLE_ENTITY_CODE
        assert response.reason == EXPECTED_UNPROCESSABLE_ENTITY_REASON

    def test_min_n_nft(self, pool_meta):
        """
        Expects a validation error, because n_nft must be in the range [1, 600]
        """
        response = client.post(
            f'{API_PREFIX}/{PRICING}',
            headers={"Content-Type": "application/json"},
            json={
                "endpoint_id": 0,
                "pool_id": "cc251a50-a1ac-4ddc-92a8-2bdb57df29ab",
                "n_nft": 0,
                "pools": pool_meta
            }
        )
        assert response.status_code == EXPECTED_UNPROCESSABLE_ENTITY_CODE
        assert response.reason == EXPECTED_UNPROCESSABLE_ENTITY_REASON

    def test_max_n_nft(self, pool_meta):
        """
        Expects a validation error, because n_nft must be in the range [1, 600]
        """
        response = client.post(
            f'{API_PREFIX}/{PRICING}',
            headers={"Content-Type": "application/json"},
            json={
                "endpoint_id": 0,
                "pool_id": "cc251a50-a1ac-4ddc-92a8-2bdb57df29ab",
                "n_nft": 601,
                "pools": pool_meta
            }
        )
        assert response.status_code == EXPECTED_UNPROCESSABLE_ENTITY_CODE
        assert response.reason == EXPECTED_UNPROCESSABLE_ENTITY_REASON
