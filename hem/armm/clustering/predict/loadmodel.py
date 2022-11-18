
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

import pathlib
import joblib

from hem.armm.clustering.model.pipelinemodel import pipeline
from hem.armm.clustering.model.gridsearch import gridsearch


def loadmodel(model_address: str):
    file = pathlib.Path(model_address)
    if not file.exists():
        raise FileNotFoundError(f'{file.as_posix()} does not exist!')
    else:
        return joblib.load(model_address)
