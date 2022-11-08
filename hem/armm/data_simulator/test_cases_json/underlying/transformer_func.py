SECONDS_IN_DAY = 86_400.


def create_transformer_input(nft):
    """

    Parameters
    ----------
    nft: the nft to be transformed

    Returns
    -------
    a dictionary (json) as the input received for data transformer api for each nft

    """
    return {"nft_id": nft.nft_id,
            "msg_type": nft.nft_state,
            "country": nft.country,
            "first_subdivision": nft.first_subdivision,
            "minting_time": nft.transaction_time[0],
            "transaction_id": nft.transaction_id,
            "transaction_time": nft.transaction_time,
            "owner": nft.owner,
            "price": nft.last_price,
            }


def create_transformer_output(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of nfts to be transformed

    Returns
    -------
    a dictionary (json) as the output of the data transformation api

    """
    response = {"nft_id": [],
                "current_owner": [],
                "nft_age": [],
                "num_owners": [],
                "avg_price": [],
                "last_price": [],
                "num_price_chg": [],
                "nft_state": [],
                "latitude": [],
                "longitude": [],
                }
    for nft in list_nfts:
        response["nft_id"].append(nft.nft_id)
        response["current_owner"].append(nft.owner[-1])
        response["nft_age"].append(nft.nft_age)
        response["num_owners"].append(len(nft.owner))
        response["avg_price"].append(nft.avg_price)
        response["last_price"].append(nft.last_price[-1])
        response["num_price_chg"].append(nft.num_price_chg)
        response["nft_state"].append(nft.nft_state[-1])
        response["latitude"].append(nft.latitude)
        response["longitude"].append(nft.longitude)
    return response
