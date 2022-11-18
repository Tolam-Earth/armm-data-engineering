
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

import json
import time
import pycountry
import numpy as np
from geopy.geocoders import Nominatim

from hem.armm.data_simulator.test_cases_json.underlying.NFTClass import NFTClass


def convert_subdivision_to_gps(country: str, first_subdivision: str):
    """

    Parameters
    ----------
    country: ISO 3166 Alpha-3 country code standard
    first_subdivision: ISO 3166-1 up to three alphanumeric characters

    Returns
    -------
    dictionary: "latitude", and "longitude" 7 decimals
    """
    geolocator = Nominatim(user_agent="hem-armm")
    country_alpha_2 = pycountry.countries.get(alpha_3=country).alpha_2
    location = geolocator.geocode(f"{country_alpha_2}-{first_subdivision}", country_codes=country_alpha_2)
    time.sleep(1.)
    return np.round(location.latitude, decimals=7), np.round(location.longitude, decimals=7)


def load_minted(json_file, count):
    """

    Parameters
    ----------
    json_file: str path to json file
    count: number of nfts to load from json file

    Returns
    -------
    list of the loaded MINTED nft classes

    """
    list_of_lists = json.load(open(json_file, ))
    minted_items = []
    temp_gps_coords = {}
    for list_nfts in list_of_lists:
        for nft in list_nfts:

            if f"{nft['country']}-{nft['first_subdivision']}" not in temp_gps_coords.keys():
                temp_gps_coords[f"{nft['country']}-{nft['first_subdivision']}"] = convert_subdivision_to_gps(
                    country=nft["country"], first_subdivision=nft["first_subdivision"])

            minted_items.append(NFTClass(token_id=nft['nft_id']['token_id'],
                                         serial_number=nft['nft_id']['serial_num'],
                                         transaction_id=nft["transaction_id"],
                                         transaction_time_seconds=int(nft['minting_time'].split(".")[0]),
                                         transaction_time_nano=int(nft['minting_time'].split(".")[1]),
                                         transaction_memo=nft["transaction_memo"],
                                         minting_owner=nft["minting_owner"],
                                         country=nft["country"],
                                         first_subdivision=nft["first_subdivision"],
                                         latitude=temp_gps_coords[f"{nft['country']}-{nft['first_subdivision']}"][0],
                                         longitude=temp_gps_coords[f"{nft['country']}-{nft['first_subdivision']}"][1],
                                         project_category=nft["project_category"],
                                         project_type=nft["project_type"],
                                         vintage_year=nft["vintage_year"],
                                         device_id=nft["device_id"],
                                         guardian_id=nft["guardian_id"],
                                         ))
            if len(minted_items) == count:
                return minted_items
    return minted_items
