
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
import numpy as np
import pandas as pd


def create_pool_meta_input(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of nfts in the call for pricing requesting pool meta

    Returns
    -------
    a dictionary (json) as the input to the pool meta api

    """
    return {"nft_id": [nft.nft_id for nft in list_nfts]}


def create_pool_meta_output(pooled_list_nfts, pool_meta_address):
    """

    Parameters
    ----------
    pooled_list_nfts: the list of nfts assigned to pools to be priced

    Returns
    -------
    a list of dictionary (json) as the output of pool meta api; each element of the list forms a call to pricing api

    """
    pooled_list_nfts = pd.read_json(pooled_list_nfts)
    with open(pool_meta_address, 'r') as file:
        pool_meta = json.load(file)
    request = []
    for token_pool_id_ in np.unique(pooled_list_nfts.token_pool_id):
        temp = {"endpoint_id": 123456,
                "pool_id": token_pool_id_,
                "n_nft": sum(pooled_list_nfts.token_pool_id == token_pool_id_),
                "pools": pool_meta,
                }
        request.append(temp)
    return request
