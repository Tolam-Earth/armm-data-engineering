from numpy import random
from collections import defaultdict

from hem.armm.data_simulator.test_cases_json.underlying.minted_func import MAX_TRANSACTION_SECONDS, \
    MIN_TRANSACTION_NANO, MAX_TRANSACTION_NANO


def create_listed(list_tolist_nfts):
    """

    Parameters
    ----------
    list_tolist_nfts: the list of nfts to be LISTED in the market

    Returns
    -------
    list of nfts with updated state as LISTED. the listing price is randomly drawn from the uniform distribution of
    [min_recommended price , max_recommended price + ( max_recommended - min_recommended)]

    """
    visited_owners = defaultdict(lambda: {"transaction_time_seconds": 0., "random": False})
    for nft in list_tolist_nfts:
        visited_owners[nft.owner[-1]]["transaction_time_seconds"] = max(
            visited_owners[nft.owner[-1]]["transaction_time_seconds"], nft.transaction_time_seconds[-1])
    for idx, nft in enumerate(list_tolist_nfts):
        if not visited_owners[nft.owner[-1]]["random"]:
            visited_owners[nft.owner[-1]]["transaction_time_seconds"] = random.randint(
                visited_owners[nft.owner[-1]]["transaction_time_seconds"], MAX_TRANSACTION_SECONDS)
            visited_owners[nft.owner[-1]]["transaction_time_nanos"] = random.randint(MIN_TRANSACTION_NANO,
                                                                                     MAX_TRANSACTION_NANO)
            visited_owners[nft.owner[-1]]["random"] = True
        nft.transaction_time_seconds.append(visited_owners[nft.owner[-1]]["transaction_time_seconds"])
        nft.transaction_time_nano.append(visited_owners[nft.owner[-1]]["transaction_time_nanos"])
        nft.transaction_time.append({"seconds": visited_owners[nft.owner[-1]]["transaction_time_seconds"],
                                     "nanos": visited_owners[nft.owner[-1]]["transaction_time_nanos"]})
        nft.transaction_id.append(
            f"{nft.owner[-1]}-{visited_owners[nft.owner[-1]]['transaction_time_seconds']}-{visited_owners[nft.owner[-1]]['transaction_time_nanos']}")
        nft.num_price_chg += 1
        nft.nft_state.append("LISTED")
        nft.listing_price = random.randint(low=nft.min_price_usd_cents, high=nft.max_price_usd_cents + (
            nft.max_price_usd_cents - nft.min_price_usd_cents) +1 )
        list_tolist_nfts[idx] = nft
    return list_tolist_nfts
