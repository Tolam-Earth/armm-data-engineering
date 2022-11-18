
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

import pandas as pd

CATEGORICAL_COLUMNS = ['country', 'project_category', 'project_type']


def generate_categorypool_list(data: pd.DataFrame) -> list:
    categorypool_list = []
    for categorypool_name in CATEGORICAL_COLUMNS:
        temp = sorted(data[categorypool_name].unique().tolist())
        categorypool_list.extend(temp)
    return categorypool_list


def generate_pool_name(categorypool_list: list, pool_id: str) -> str:
    """ generates a pool name by concatenating categories and pool id separated by underscores """
    return "_".join([*categorypool_list, pool_id])
