# -*- coding: utf-8 -*-

# Copyright (c) 2022 Tolam Earth
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import os
import json
import argparse

from hem.armm.data_simulator.test_cases_json.underlying.load_minted import load_minted
from hem.armm.data_simulator.test_cases_json.underlying.minted_func import create_minted, create_nft_details_schema
from hem.armm.data_simulator.test_cases_json.underlying.transformer_func import create_transformer_input, \
    create_transformer_output
from hem.armm.data_simulator.test_cases_json.underlying.pooling_classifier_func import create_pooling_input, \
    create_pooling_output
from hem.armm.data_simulator.test_cases_json.underlying.toke_attribute_db_func import create_attribute_db_input
from hem.armm.data_simulator.test_cases_json.underlying.nft_pool_meta_func import create_pool_meta_input, \
    create_pool_meta_output
from hem.armm.data_simulator.test_cases_json.underlying.pricing_func import create_pricing_output
from hem.armm.data_simulator.test_cases_json.underlying.pricing_db_func import create_pricing_db_input
from hem.armm.data_simulator.test_cases_json.underlying.listed_func import create_listed
from hem.armm.data_simulator.test_cases_json.underlying.marketplace_state_func import create_marketplace_state_output
from hem.armm.data_simulator.test_cases_json.underlying.query_armm_func import create_query_armm_input, \
    create_query_armm_output
from hem.armm.data_simulator.test_cases_json.underlying.buy_agent_func import create_buy_agent_input

MAX_N_NFTS = 600


def get_arguments():
    def limit_n_simulations(input_n_simulations):
        input_n_simulations = int(input_n_simulations)
        if input_n_simulations > MAX_N_NFTS:
            raise argparse.ArgumentTypeError(f"Maximum number of nfts is {MAX_N_NFTS}")
        return input_n_simulations

    parser = argparse.ArgumentParser()
    parser.add_argument("n_simulations", type=limit_n_simulations,
                        help=f"the total number of to-be-simulated nfts; must be <={MAX_N_NFTS}")
    parser.add_argument("model_address", type=str, help="the path to the trained pipeline")
    parser.add_argument("pool_meta_address", type=str, help="the path metadata of all pools")
    parser.add_argument("--minted_nfts_path",
                        help="path to the json file including minted NFTs",
                        type=str, default=None)
    parser.add_argument("--saving_path",
                        help="path to where the data will be created",
                        type=str, default='.')
    args = parser.parse_args()
    return args.n_simulations, args.model_address, args.pool_meta_address, args.minted_nfts_path, args.saving_path


def create_folders(saving_path):
    for folder in ['1-ARMM_Ingests_Minted_NFT_Flow/1-minted',
                   '1-ARMM_Ingests_Minted_NFT_Flow/2-transformer/input',
                   '1-ARMM_Ingests_Minted_NFT_Flow/2-transformer/output',
                   '1-ARMM_Ingests_Minted_NFT_Flow/3-pooling_classifier/input',
                   '1-ARMM_Ingests_Minted_NFT_Flow/3-pooling_classifier/output',
                   '1-ARMM_Ingests_Minted_NFT_Flow/4-token_details_db',
                   '2-ARMM_Pricing_Workflow/1-nft_pool_meta/input',
                   '2-ARMM_Pricing_Workflow/1-nft_pool_meta/output',
                   '2-ARMM_Pricing_Workflow/2-pricing/input',
                   '2-ARMM_Pricing_Workflow/2-pricing/output',
                   '2-ARMM_Pricing_Workflow/3-pricing_db',
                   '3-ARMM_Buy_Agent_Flow_for_MVP/1-marketplace_state',
                   '3-ARMM_Buy_Agent_Flow_for_MVP/2-query_ARMM/input',
                   '3-ARMM_Buy_Agent_Flow_for_MVP/2-query_ARMM/output',
                   '3-ARMM_Buy_Agent_Flow_for_MVP/3-buy_agent/input']:
        file_name = f"{saving_path}/cases/{folder}/"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)


if __name__ == '__main__':
    n_simulations, model_address, pool_meta_address, minted_nfts_path, saving_path = get_arguments()

    create_folders(saving_path)

    name = "test"

    ### ARMM Ingests Minted NFT Flow ###

    # load Minted NFTs
    if minted_nfts_path is not None and n_simulations < MAX_N_NFTS:
        list_minted_nfts = load_minted(minted_nfts_path, count=MAX_N_NFTS - n_simulations)
        # simulate MINTED NFTs
        list_minted_nfts.extend(create_minted(n_simulations=n_simulations))
    else:
        # simulate MINTED NFTs
        list_minted_nfts = create_minted(n_simulations=n_simulations)

    json_object = [create_nft_details_schema(nft) for nft in list_minted_nfts]
    with open(f"{saving_path}/cases/1-ARMM_Ingests_Minted_NFT_Flow/1-minted/{name}.json", "w+") as outfile:
        json.dump(json_object, outfile, indent=2)

    ### no history processing for MINTED tokens ###

    # data transformation
    transformer_input = [create_transformer_input(nft) for nft in list_minted_nfts]
    with open(f"{saving_path}/cases/1-ARMM_Ingests_Minted_NFT_Flow/2-transformer/input/{name}.json", "w+") as outfile:
        json.dump(transformer_input, outfile, indent=2)
    transformer_output = create_transformer_output(list_minted_nfts)
    with open(f"{saving_path}/cases/1-ARMM_Ingests_Minted_NFT_Flow/2-transformer/output/{name}.json", "w+") as outfile:
        json.dump(transformer_output, outfile, indent=2)

    # pool classification
    pooling_input = create_pooling_input(list_minted_nfts)
    with open(f"{saving_path}/cases/1-ARMM_Ingests_Minted_NFT_Flow/3-pooling_classifier/input/{name}.json", "w+") as outfile:
        json.dump(pooling_input, outfile, indent=2)
    # pool_id, name_pool, and pooling_version are updated in the MINTED nfts
    list_minted_nfts, pooling_output = create_pooling_output(
        list_minted_nfts, model_address=model_address)
    pooling_output = json.dumps(pooling_output, indent=2)
    with open(f"{saving_path}/cases/1-ARMM_Ingests_Minted_NFT_Flow/3-pooling_classifier/output/{name}.json", "w+") as outfile:
        outfile.write(pooling_output)

    # token details write to database
    token_details_db = create_attribute_db_input(list_minted_nfts)
    with open(f"{saving_path}/cases/1-ARMM_Ingests_Minted_NFT_Flow/4-token_details_db/{name}-db.json", "w+") as outfile:
        json.dump(token_details_db, outfile, indent=2)

    ### ARMM Pricing Workflow ###

    # pool membership for the NFTs
    nft_pool_meta_input = create_pool_meta_input(list_minted_nfts)
    with open(f"{saving_path}/cases/2-ARMM_Pricing_Workflow/1-nft_pool_meta/input/{name}.json", "w+") as outfile:
        json.dump(nft_pool_meta_input, outfile, indent=2)
    # NFTs with same pool form their own pricing request
    temp_nft_pool_meta_output = create_pool_meta_output(
        pooling_output, pool_meta_address=pool_meta_address)
    with open(f"{saving_path}/cases/2-ARMM_Pricing_Workflow/1-nft_pool_meta/output/{name}.json", "w+") as outfile:
        json.dump(temp_nft_pool_meta_output, outfile, indent=2)

    # request the min and max prices for the NFT
    with open(f"{saving_path}/cases/2-ARMM_Pricing_Workflow/2-pricing/input/{name}.json", "w+") as outfile:
        json.dump(temp_nft_pool_meta_output, outfile, indent=2)
    # min_price_usd_cents, and max_price_usd_cents are updated in the MINTED nfts
    list_pricing_output, list_minted_nfts = create_pricing_output(temp_nft_pool_meta_output, list_minted_nfts)
    with open(f"{saving_path}/cases/2-ARMM_Pricing_Workflow/2-pricing/output/{name}.json", "w+") as outfile:
        json.dump(list_pricing_output, outfile, indent=2)

    # pricing write to database
    pricing_db = create_pricing_db_input(list_minted_nfts)
    with open(f"{saving_path}/cases/2-ARMM_Pricing_Workflow/3-pricing_db/{name}-db.json", "w+") as outfile:
        json.dump(pricing_db, outfile, indent=2)

    ### ARMM Buy Agent Flow for MVP ###
    list_listed_nfts = create_listed(list_minted_nfts)

    # token marketplace state topic
    token_marketplace_state_topic = create_marketplace_state_output(list_listed_nfts)
    with open(f"{saving_path}/cases/3-ARMM_Buy_Agent_Flow_for_MVP/1-marketplace_state/{name}.json", "w+") as outfile:
        json.dump(token_marketplace_state_topic, outfile, indent=2)

    # Query to ARMM Databases
    list_query_armm_input = create_query_armm_input(list_listed_nfts)
    with open(f"{saving_path}/cases/3-ARMM_Buy_Agent_Flow_for_MVP/2-query_ARMM/input/{name}.json", "w+") as outfile:
        json.dump(list_query_armm_input, outfile, indent=2)

    list_query_armm_output = create_query_armm_output(list_listed_nfts)
    with open(f"{saving_path}/cases/3-ARMM_Buy_Agent_Flow_for_MVP/2-query_ARMM/output/{name}.json", "w+") as outfile:
        json.dump(list_query_armm_output, outfile, indent=2)

    # Buy Agent Token Message
    list_buy_agent_input = create_buy_agent_input(list_listed_nfts)
    with open(f"{saving_path}/cases/3-ARMM_Buy_Agent_Flow_for_MVP/3-buy_agent/input/{name}.json", "w+") as outfile:
        json.dump(list_buy_agent_input, outfile, indent=2)
