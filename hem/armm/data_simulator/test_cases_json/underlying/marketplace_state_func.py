def create_marketplace_state_output(list_nfts):
    """

    Parameters
    ----------
    list_nfts: the list of LISTED nfts to form marketplace state

    Returns
    -------
    a list of dictionary (json) for each nft as the marketplace state output

    """
    response = []
    for nft in list_nfts:
        temp = {
            "msg_type": nft.nft_state[-1],
            "nft_id": nft.nft_id,
            "owner": nft.owner[-1],
            "listing_price": nft.listing_price,
            "purchase_price": nft.purchase_price,
            "transaction_id": nft.transaction_id[-1],
            "transaction_time": nft.transaction_time[-1],
        }
        response.append(temp)
    return response
