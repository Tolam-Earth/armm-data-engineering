import json
import argparse
import numpy as np

from hem.armm.pricing.pricing import arm_sells_price, arm_buys_price

CONSTANT_R = 10000000.


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("pool_id", help="pool id of NFTs to be priced")
    parser.add_argument("n_nft", type=int, help="number of NFTs in the current call", )
    parser.add_argument("pool_meta", type=str, help="the metadata of all pools")
    parser.add_argument("--currency_reserve", type=float,
                        help="quantity of a reserve currency in USD.cents", default=CONSTANT_R)
    args = parser.parse_args()
    return args.pool_id, args.n_nft, args.pool_meta, args.currency_reserve


def main(pool_id, n_nft: int, pool_meta: list, r: float = CONSTANT_R) -> dict[str: float]:
    pool_index = next((index for (index, _pool) in enumerate(pool_meta) if _pool["id"] == pool_id))
    x_matrix = np.transpose(np.array([_pool['mean_pool'] for _pool in pool_meta], dtype=float))
    q = np.array([_pool['n_pool'] for _pool in pool_meta], dtype=int)

    min_price = arm_buys_price(x_matrix, q, pool_index, n_nft, r)
    max_price = arm_sells_price(x_matrix, q, pool_index, n_nft, r)

    return {"min_price_usd_cents": min_price/n_nft, "max_price_usd_cents": max_price/n_nft}


if __name__ == '__main__':
    pool_id, n_nft, pool_meta, currency_reserve = get_arguments()
    with open(pool_meta, 'r') as file:
        pool_meta = json.load(file)
    pricing = main(pool_id, n_nft, pool_meta, r=currency_reserve)
    # print(pricing)
    # save: the pricing as JSON file
    with open('pricing.json', 'w') as file:
        json.dump(pricing, file, indent=4)
