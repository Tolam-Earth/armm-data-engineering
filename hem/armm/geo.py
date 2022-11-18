
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

import logging
import pkg_resources
from functools import cache
from typing import Optional, Union, Tuple

import pandas as pd


logger = logging.getLogger(__name__)


class GeoCoder:
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or pkg_resources.resource_filename('hem', 'armm/data/global-first-subdivision.csv')
        self.df = self.load_geocoder()

    def load_geocoder(self) -> pd.DataFrame:
        logger.info(f'Loading geocoder from {self.file_path}')
        return pd.read_csv(self.file_path)

    @cache
    def geocode(self, country: str, first_subdivision: Union[int, str]) -> Tuple[Optional[float], Optional[float]]:
        """

        :param country:
        :type country: str
        :param first_subdivision: 2-3
        :type first_subdivision: str or int
        :return: (longitude, latitude) or (None, None)
        :rtype: (float, float) or (None, None)
        """
        result = self.df.loc[
            (self.df['gu_a3'] == country) & (self.df['first_subdivision'] == str(first_subdivision)),
            ['repr_longitude', 'repr_latitude']
        ]
        if len(result) == 1:
            return result.values[0]
        elif len(result) > 1:
            logger.warning(f'{len(result)=}, returning the first record found')
            return result.values[0]
        else:
            logger.error(f'{len(result)=}, returning (None, None)')
            return None, None
