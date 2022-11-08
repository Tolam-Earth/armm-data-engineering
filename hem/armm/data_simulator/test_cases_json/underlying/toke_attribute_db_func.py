
def create_attribute_db_input(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of nfts to be written to database

    Returns
    -------
    a list of dictionary (json) for each nft as the table of token attributes to be written to database

    """
    response = []
    for nft in list_nfts:
        temp = {
            "nft_id": nft.nft_id,
            "transaction_id": nft.transaction_id[-1],
            "transaction_time": nft.transaction_time[-1],
            "minting_owner": nft.minting_owner,
            "owner": nft.owner[-1],
            "country": nft.country,
            "first_subdivision": nft.first_subdivision,
            "latitude": nft.latitude,
            "longitude": nft.longitude,
            "project_category": nft.project_category,
            "project_type": nft.project_type,
            "vintage_year": nft.vintage_year,
            "nft_age": nft.nft_age,
            "num_owners": nft.num_owners,
            "avg_price": nft.avg_price,
            "last_price": nft.last_price[-1],
            "num_price_chg": nft.num_price_chg,
            "nft_state": nft.nft_state[-1],
            "token_pool_id": nft.token_pool_id[-1],
            "name_pool": nft.name_pool[-1],
            "pooling_version": nft.pooling_version[-1],
        }
        response.append(temp)
    return response
