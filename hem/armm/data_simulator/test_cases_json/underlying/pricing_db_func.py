
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
