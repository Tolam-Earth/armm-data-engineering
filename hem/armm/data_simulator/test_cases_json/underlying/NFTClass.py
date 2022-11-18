
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

class NFTClass:
    def __init__(self, token_id, serial_number, transaction_id, transaction_time_seconds, transaction_time_nano,
                 minting_owner, country, first_subdivision,
                 latitude, longitude, project_category, project_type, vintage_year, device_id, guardian_id,
                 owner=None, nft_age=0, num_owners=1, avg_price=0, last_price=0, num_price_chg=0,
                 nft_state="MINTED", min_price_usd_cents=0, max_price_usd_cents=0, transaction_memo=None):
        """

        Parameters
        ----------
        token_id
        serial_number
        transaction_id
        transaction_time_seconds
        transaction_time_nano
        minting_owner
        country
        first_subdivision
        latitude
        longitude
        project_category
        project_type
        vintage_year
        device_id
        guardian_id
        owner
        nft_age
        num_owners
        avg_price
        last_price
        num_price_chg
        nft_state
        min_price_usd_cents
        max_price_usd_cents
        """
        self.token_id = token_id
        self.serial_number = serial_number
        self.nft_id = {"token_id": str(token_id),
                       "serial_number": int(serial_number),
                       }
        self.transaction_id = [transaction_id]
        self.transaction_time_seconds = [transaction_time_seconds]
        self.transaction_time_nano = [transaction_time_nano]
        self.transaction_time = [{"seconds": transaction_time_seconds, "nanos": transaction_time_nano}]
        if transaction_memo is None:
            self.transaction_memo = f"{transaction_time_seconds}.{transaction_time_nano}"
        else:
            self.transaction_memo = transaction_memo
        self.minting_owner = minting_owner
        self.owner = [minting_owner] if owner is None else [owner]
        self.country = country
        self.first_subdivision = first_subdivision
        self.latitude = latitude
        self.longitude = longitude
        self.project_category = project_category
        self.project_type = project_type
        self.vintage_year = vintage_year
        self.nft_age = nft_age
        self.num_owners = num_owners
        self.avg_price = avg_price
        self.last_price = [last_price]
        self.num_price_chg = num_price_chg
        self.nft_state = [nft_state]
        self.token_pool_id = []
        self.name_pool = []
        self.pooling_version = []
        self.device_id = device_id
        self.guardian_id = guardian_id

        self.min_price_usd_cents = min_price_usd_cents
        self.max_price_usd_cents = max_price_usd_cents

        self.listing_price = -100
        self.purchase_price = -100
