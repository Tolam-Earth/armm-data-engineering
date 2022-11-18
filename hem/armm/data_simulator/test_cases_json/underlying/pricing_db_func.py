
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

def create_pricing_db_input(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of nfts to be written to database

    Returns
    -------
    a list of dictionary (json) for each nft with the price recommendations to be written to the database

    """
    response = []
    for nft in list_nfts:
        temp = {
            "nft_id": nft.nft_id,
            "min_price_usd_cents": nft.min_price_usd_cents,
            "max_price_usd_cents": nft.max_price_usd_cents,
        }
        response.append(temp)
    return response
