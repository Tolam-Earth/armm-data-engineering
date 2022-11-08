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
