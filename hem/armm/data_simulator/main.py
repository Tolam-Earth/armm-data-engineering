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

import sys

import pandas as pd
import numpy as np
from numpy import random
from pydantic import BaseModel, Field
import pycountry
from geopy.geocoders import Nominatim

MISSING_VALUE = 0


class NftMintDetails(BaseModel):
    country: str = Field(..., max_length=3)
    first_subdivision: str
    latitude: float
    longitude: float
    project_category: str
    project_type: str
    vintage_year: int
    nft_age: int = Field(..., ge=0)
    num_owners: int = Field(..., ge=0)
    avg_price: float
    last_price: float
    num_price_chg: int
    nft_state: str


class FakeNftPool:
    def __init__(self):
        self.country = ['BGR', 'ETH', 'FRA', 'GBR', 'GIN', 'GTM', 'HND', 'IDN', 'IND',
                        'KEN', 'KHM', 'MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']
        self.GPS_coordinates = self.country_to_gps()
        # self.project_category = ['WASTE_MGMT', 'RENEW_ENERGY',
        #                          'FOREST_CONSERV', 'COMM_ENRGY_EFF']
        self.project_type = ['EMM_RED', 'SOLAR', 'WIND', 'HYDRO', 'AGG_LAND_MGMT', 'COOK_STV', 'WATER', 'BIOGAS']
        self.avg_price_std = np.sqrt(5)
        self.last_price_std = np.sqrt(5)
        self.nft_age_lambda = 15
        self.num_owners_lambda = 1
        self.num_price_chg_lambda = 1

    def project_category(self, project):
        if project in ['EMM_RED']:
            return 'WASTE_MGMT'
        elif project in ['SOLAR', 'WIND', 'HYDRO']:
            return 'RENEW_ENERGY'
        elif project in ['AGG_LAND_MGMT']:
            return 'FOREST_CONSERV'
        elif project in ['COOK_STV', 'WATER', 'BIOGAS']:
            return 'COMM_ENRGY_EFF'

    def price_mean(self, country, project_category, project_type):
        price = 0.
        if project_category == 'COMM_ENRGY_EFF':
            price = 25.
            if np.isin(country, ['BGR', 'ETH', 'FRA', 'GBR', 'GIN']):
                price += 10
            elif np.isin(country, ['MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']):
                price += 20
        elif project_category == 'FOREST_CONSERV':
            price = 30.
            if np.isin(country, ['BGR', 'ETH', 'FRA', 'GBR', 'GIN']):
                price += 3
            elif np.isin(country, ['MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']):
                price += 5
        elif project_category == 'RENEW_ENERGY':
            price = 25.
            if np.isin(country, ['BGR', 'ETH', 'FRA', 'GBR', 'GIN']):
                price += 1.5
            elif np.isin(country, ['MMR', 'MOZ', 'NIC', 'PER', 'RWA', 'USA']):
                price += 3
        elif project_category == 'WASTE_MGMT':
            price = 20.
        return price

    def country_to_gps(self):
        gps_coordinates = {}
        geolocator = Nominatim(user_agent="temp")
        for country_alpha_3 in self.country:
            country_alpha_2 = pycountry.countries.get(alpha_3=country_alpha_3).alpha_2
            location = geolocator.geocode(country_alpha_2, country_codes=country_alpha_2)
            gps_coordinates[country_alpha_3] = [location.latitude, location.longitude]
        return gps_coordinates

    def creating_fake_nft(self, missing_allowed=True):
        country = random.choice(self.country)
        latitude = self.GPS_coordinates[country][0]
        longitude = self.GPS_coordinates[country][1]
        project_type = random.choice(self.project_type)
        project_category = self.project_category(project_type)
        nft_age = random.poisson(lam=self.nft_age_lambda)
        num_owners = 1 + random.poisson(lam=self.num_owners_lambda)
        if missing_allowed and num_owners == 1 and random.choice([False, True]):
            avg_price = MISSING_VALUE
            last_price = MISSING_VALUE
            num_price_chg = 0
        else:
            avg_price = np.abs(random.normal(loc=self.price_mean(
                country, project_category, project_type), scale=self.avg_price_std))
            last_price = np.abs(random.normal(
                loc=avg_price, scale=self.last_price_std))
            num_price_chg = random.poisson(lam=self.num_price_chg_lambda)
        return NftMintDetails(
            country=country,
            first_subdivision='N/A',
            latitude=latitude,
            longitude=longitude,
            project_category=project_category,
            project_type=project_type,
            vintage_year=0,
            nft_age=nft_age,
            num_owners=num_owners,
            avg_price=avg_price,
            last_price=last_price,
            num_price_chg=num_price_chg,
            nft_state='N/A')


def main(n=10000, missing_allowed=True):
    """
    :param n: number of simulated data to generate
    :param missing_allowed: whether it is allowed to have missing data in simulation
    """
    faker = FakeNftPool()
    results = [faker.creating_fake_nft(missing_allowed=missing_allowed).dict()
               for _ in range(n)]
    data = pd.DataFrame(results)
    data.to_csv('simulated_data.csv', index=False)


if __name__ == '__main__':
    n = 5000
    missing_allowed = False
    if len(sys.argv) > 1:
        n = sys.argv[1]
        if len(sys.argv) > 2:
            missing_allowed = sys.argv[2]
    main(n=n, missing_allowed=missing_allowed)
