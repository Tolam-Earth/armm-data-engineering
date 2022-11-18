
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
