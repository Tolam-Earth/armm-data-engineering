import numpy as np
import pandas as pd

from hem.armm.clustering.predict.main import main

pd.options.mode.chained_assignment = None


def create_pooling_input(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of nfts to be assigned to pools

    Returns
    -------
    a dictionary (json) as the input to the pool classifier api

    """
    request = {"nft_id": [],
               "transaction_id": [],
               "transaction_time": [],
               "minting_owner": [],
               "owner": [],
               "country": [],
               "first_subdivision": [],
               "latitude": [],
               "longitude": [],
               "project_category": [],
               "project_type": [],
               "vintage_year": [],
               "nft_age": [],
               "num_owners": [],
               "avg_price": [],
               "last_price": [],
               "num_price_chg": [],
               "nft_state": [],
               }

    for nft in list_nfts:
        request["nft_id"].append(nft.nft_id)
        request["transaction_id"].append(nft.transaction_id[-1])
        request["transaction_time"].append(
            {"seconds": nft.transaction_time_seconds[-1],
             "nanos": nft.transaction_time_nano[-1],
             })
        request["minting_owner"].append(nft.minting_owner)
        request["owner"].append(nft.owner[-1])
        request["country"].append(nft.country)
        request["first_subdivision"].append(nft.first_subdivision)
        request["latitude"].append(nft.latitude)
        request["longitude"].append(nft.longitude)
        request["project_category"].append(nft.project_category)
        request["project_type"].append(nft.project_type)
        request["vintage_year"].append(nft.vintage_year)
        request["nft_age"].append(nft.nft_age)
        request["num_owners"].append(nft.num_owners)
        request["avg_price"].append(nft.avg_price)
        request["last_price"].append(nft.last_price[-1])
        request["num_price_chg"].append(nft.num_price_chg)
        request["nft_state"].append(nft.nft_state[-1])

    return request


def create_pooling_output(list_nfts, model_address):
    """

    Parameters
    ----------
    list_nfts: the list of nfts to be assigned to pools
    model_address: path to the pkl file containing the clustering model

    Returns
    -------
    a dictionary (json) as the output of the pool classifier api

    """
    data = pd.DataFrame.from_dict(create_pooling_input(list_nfts))
    prediction = main(model_address, data)
    prediction = prediction[
        ["nft_id", "transaction_id", "transaction_time", "token_pool_id", "name_pool", "pooling_version"]]
    for idx, nft in enumerate(list_nfts):
        temp = prediction.loc[prediction['nft_id'] == nft.nft_id]
        nft.token_pool_id.append(temp.token_pool_id.values[0])
        nft.name_pool.append(temp.name_pool.values[0])
        nft.pooling_version.append(temp.pooling_version.values[0])
        list_nfts[idx] = nft
    prediction.loc[:, 'token_pool_id'] = prediction.token_pool_id.apply(str)
    return list_nfts, prediction.to_dict(orient="list")
