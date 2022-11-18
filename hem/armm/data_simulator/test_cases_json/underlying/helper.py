
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

import time
import numpy as np
from numpy import random
import pycountry
from geopy.geocoders import Nominatim


def convert_country_to_gps(country_list):
    gps_coordinates = {}
    geolocator = Nominatim(user_agent="hem-armm")
    for country_alpha_3 in country_list.keys():
        gps_coordinates[country_alpha_3] = {}
        country_alpha_2 = pycountry.countries.get(alpha_3=country_alpha_3).alpha_2
        for subdivision in country_list[country_alpha_3]:
            location = geolocator.geocode(f"{country_alpha_2}-{subdivision}", country_codes=country_alpha_2)
            gps_coordinates[country_alpha_3][subdivision] = [location.latitude, location.longitude]
            time.sleep(1.)
    return gps_coordinates


def define_project_type(project):
    if project == 'WASTE_MGMT':
        return random.choice(['EMM_RED'])
    elif project == 'RENEW_ENERGY':
        return random.choice(['SOLAR', 'WIND', 'HYDRO'])
    elif project == 'FOREST_CONSERV':
        return random.choice(['AGG_LAND_MGMT'])
    elif project == 'COMM_ENRGY_EFF':
        return random.choice(['COOK_STV', 'WATER', 'BIOGAS'])


def define_price_mean(country, project_category, project_type):
    price = 0.
    if project_category == 'COMM_ENRGY_EFF':
        price = 15.
        if np.isin(country, ['BGR', 'ETH', 'FRA', 'GBR', 'GIN']):
            price += 10
        elif np.isin(country, ['MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']):
            price += 20
    elif project_category == 'FOREST_CONSERV':
        price = 20.
        if np.isin(country, ['BGR', 'ETH', 'FRA', 'GBR', 'GIN']):
            price += 3
        elif np.isin(country, ['MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']):
            price += 5
    elif project_category == 'RENEW_ENERGY':
        price = 15.
        if np.isin(country, ['BGR', 'ETH', 'FRA', 'GBR', 'GIN']):
            price += 1.5
        elif np.isin(country, ['MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']):
            price += 3
    elif project_category == 'WASTE_MGMT':
        price = 10.
    return price


# COUNTRY_LIST = ['BGR', 'ETH', 'FRA', 'GBR', 'IND',
#                 'KEN', 'KHM', 'MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']
COUNTRY_FIRST_SUBDIVISION_DICT = {
    'BGR': ["01"],
    'ETH': ["TI"],
    'FRA': ["75C"],
    'GBR': ["BEX"],
    'IND': ["DL"],
    'KEN': ["44"],
    'USA': ["AZ"],
}
PROJECT_CAT_LIST = ['WASTE_MGMT',
                    'RENEW_ENERGY',
                    'FOREST_CONSERV',
                    'COMM_ENRGY_EFF',
                    ]

GPS_COORDINATES = convert_country_to_gps(COUNTRY_FIRST_SUBDIVISION_DICT)
