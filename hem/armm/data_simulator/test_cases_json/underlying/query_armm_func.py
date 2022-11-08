def create_query_armm_input(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of LISTED nfts to be queried from the ARMM

    Returns
    -------
    a list of dictionary (json) for each nft as query input to ARMM

    """
    return [{"nft_id": nft.nft_id} for nft in list_nfts]


def create_query_armm_output(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of LISTED nfts queried from the ARMM

    Returns
    -------
    a list of dictionary (json) for each nft with ARMM query output

    """
    response = []
    for nft in list_nfts:
        temp = {
            "nft_id": nft.nft_id,
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
