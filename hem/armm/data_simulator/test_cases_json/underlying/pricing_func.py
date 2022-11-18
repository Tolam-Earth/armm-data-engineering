
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

from hem.armm.pricing.main import main


def create_pricing_output(list_pricing_requests, list_nfts):
    """

    Parameters
    ----------
    list_pricing_requests: the list of dictionary (json) containing calls to pricing api
    list_nfts: the list of nfts in th pricing request ( to record their prices in NFTClass)

    Returns
    -------
    list of dictionary with min and max price for each pricing request
    list of nfts (NFTClass) with updated min max prices

    """
    response = {}
    _temp_n_nft = {}
    for request in list_pricing_requests:
        response[request["pool_id"]] = main(pool_id=request["pool_id"], n_nft=request["n_nft"],
                                            pool_meta=request["pools"])
        _temp_n_nft[request["pool_id"]] = request["n_nft"]
    for idx, nft in enumerate(list_nfts):
        nft.min_price_usd_cents = int(response[nft.token_pool_id[-1]]["min_price_usd_cents"])
        nft.max_price_usd_cents = int(response[nft.token_pool_id[-1]]["max_price_usd_cents"])
        list_nfts[idx] = nft

    return [response[request["pool_id"]] for request in list_pricing_requests], list_nfts
