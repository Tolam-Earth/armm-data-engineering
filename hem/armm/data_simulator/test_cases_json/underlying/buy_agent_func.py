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
