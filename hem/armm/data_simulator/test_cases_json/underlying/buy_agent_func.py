
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

def create_buy_agent_input(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of LISTED nfts to be passed to ARMM buy agent

    Returns
    -------
    a list of dictionary (json) for each nft as ARMM buy agent input

    """
    response = []
    for nft in list_nfts:
        temp = {
            "msg_type": nft.nft_state[-1],
            "nft_id": nft.nft_id,
            "owner": nft.owner[-1],
            "listing_price": nft.listing_price,
            "transaction_id": nft.transaction_id[-1],
            "transaction_time": nft.transaction_time[-1],
            "country": nft.country,
            "first_subdivision": nft.first_subdivision,
            "latitude": nft.latitude,
            "longitude": nft.longitude,
            "project_category": nft.project_category,
            "project_type": nft.project_type,
            "vintage_year": nft.vintage_year,
            "token_pool_id": nft.token_pool_id[-1],
            "min_price_usd_cents": nft.min_price_usd_cents,
            "max_price_usd_cents": nft.max_price_usd_cents,
        }
        response.append(temp)
    return response
