import time
from typing import Optional

import pytest
from pydantic import ValidationError

from hem.armm import nft, geo

ONE_SECOND_IN_NANOSECONDS = 1000000000
TWO_MINUTES_IN_NANOSECONDS = 120000000000


def expected_elapsed_days(time1: int, time2: int) -> int:
    """ Assumes time1 <= time2. """
    return int((time2 - time1) / nft.NANOSECONDS_PER_DAY)


class TestNftDetails:
    valid_data = {
        "nft_id": {"token_id": "1.2.3", "serial_number": 1},
        "msg_type": ["MINTED", "LISTED", "LISTED", "LISTED", ],
        "country": "USA",
        "first_subdivision": "MO",
        "minting_time": 1661400288,
        "transaction_id": ["abc12345677", "abc12345678", "abc12345679", "abc12345680"],
        "transaction_time": [
            {"seconds": 1661400288, "nanos": 335616980},
            {"seconds": 1661967010, "nanos": 335616988},
            {"seconds": 1661967145, "nanos": 335616980},
            {"seconds": 1661967300, "nanos": 335616989}
        ],
        "owner": ["0.0.45", "0.0.45", "0.0.45", "0.0.45", ],
        "price": [None, 2020, 4522, 100, ]
    }

    def test_valid_data(self):
        nft_listed_purchased_details = nft.NftDetails.parse_obj(self.valid_data)

        # mostly just testing that this is valid data with a successful parse_obj
        assert nft_listed_purchased_details.nft_id.token_id == "1.2.3"

    def test_valid_subdivision(self):
        data = self.valid_data.copy()
        data['first_subdivision'] = '75C'
        data['country'] = 'FRA'
        nft_details = nft.NftDetails.parse_obj(data)

        # mostly just testing that this is valid data with a successful parse_obj
        assert nft_details.nft_id.token_id == "1.2.3"
        assert nft_details.first_subdivision == '75C'

    def test_negative_minting_time(self):
        data = self.valid_data.copy()
        data['minting_time'] = -1

        with pytest.raises(ValidationError, match='ensure this value is greater than or equal to 0'):
            nft.NftDetails.parse_obj(data)

    def test_float_minting_time(self):
        data = self.valid_data.copy()
        data['minting_time'] = 1.55

        nft_details = nft.NftDetails.parse_obj(data)

        assert nft_details.minting_time == 1.55

    def test_float_str_minting_time(self):
        data = self.valid_data.copy()
        data['minting_time'] = "1.55"

        nft_details = nft.NftDetails.parse_obj(data)

        assert nft_details.minting_time == 1.55

    def test_negative_transaction_time(self):
        data = self.valid_data.copy()
        data['transaction_time'] = [
            {"seconds": -1, "nanos": 0},
            {"seconds": -1, "nanos": 0},
            {"seconds": 100, "nanos": 0},
        ]

        with pytest.raises(ValidationError, match='ensure this value is greater than or equal to 0'):
            nft.NftDetails.parse_obj(data)

    def test_optional_nanos(self):
        data = self.valid_data.copy()
        data['transaction_time'] = [
            {"seconds": 80, "nanos": 3},
            {"seconds": 70},
            {"seconds": 100},
            {"seconds": 300},
        ]
        nft_listed_purchased_details = nft.NftDetails.parse_obj(data)

        assert nft_listed_purchased_details.transaction_time[0].nanos == 3
        assert nft_listed_purchased_details.transaction_time[1].nanos == 0
        assert nft_listed_purchased_details.transaction_time[2].nanos == 0

    def test_lower_to_upper_strings(self):
        data = self.valid_data.copy()
        data['country'] = 'usa'
        data['first_subdivision'] = 'mo'

        nft_listed_purchased_details = nft.NftDetails.parse_obj(data)

        assert nft_listed_purchased_details.country == 'USA'
        assert nft_listed_purchased_details.first_subdivision == 'MO'

    def test_incorrect_country_code(self):
        data = self.valid_data.copy()
        data['country'] = 'US'

        with pytest.raises(ValidationError, match='string does not match regex'):
            nft.NftDetails.parse_obj(data)

        data['country'] = 'USAA'

        with pytest.raises(ValidationError, match='string does not match regex'):
            nft.NftDetails.parse_obj(data)

    def test_incorrect_length_subdivision_code(self):
        data = self.valid_data.copy()
        data['first_subdivision'] = 'M'

        with pytest.raises(ValidationError, match='string does not match regex'):
            nft.NftDetails.parse_obj(data)

        data['first_subdivision'] = 'Missouri'

        with pytest.raises(ValidationError, match='string does not match regex'):
            nft.NftDetails.parse_obj(data)

    def test_market_age(self):
        # current time - first transaction time as days
        expected = int((time.time_ns() - (1661400288 * nft.NANOSECONDS_PER_SECOND)) / nft.NANOSECONDS_PER_DAY)
        nft_details = nft.NftDetails.parse_obj(self.valid_data)
        assert nft_details.market_age == expected

    def test_minted_only(self):
        minted = {
            "nft_id": {"token_id": "1.2.3", "serial_number": 1},
            "msg_type": ["MINTED"],
            "country": "USA",
            "first_subdivision": "MO",
            "minting_time": 1661400288,
            "transaction_id": ["abc12345677"],
            "transaction_time": [
                {"seconds": 1661400288, "nanos": 335616980},
            ],
            "owner": ["0.0.45"],
            "price": [None]
        }
        details = nft.NftDetails.parse_obj(minted)

        # current time - first transaction time as days
        expected_days = int((time.time_ns() - (1661400288 * nft.NANOSECONDS_PER_SECOND)) / nft.NANOSECONDS_PER_DAY)
        assert details.market_age == expected_days

    def test_mismatched_length(self):
        data = {
            "nft_id": {"token_id": "1.2.3", "serial_number": 1},
            "msg_type": ["MINTED", "LISTED"],
            "country": "USA",
            "first_subdivision": "IL",
            "minting_time": 1661400288,
            "transaction_id": ["abc12345677", "abc12345678"],
            "transaction_time": [
                {"seconds": 1661400288, "nanos": 335616980},
            ],
            "owner": ["0.0.45"],
            "price": [None]
        }
        with pytest.raises(ValidationError, match='Lists must all be the same length!'):
            nft.NftDetails.parse_obj(data)


class TestTransformDetails:
    details = nft.NftDetails.parse_obj({
        "nft_id": {"token_id": "1.2.3", "serial_number": 1},
        "msg_type": ["MINTED", "LISTED", "LISTED", "LISTED", ],
        "country": "USA",
        "first_subdivision": "MO",
        "minting_time": 1661400288,
        "transaction_id": ["abc12345677", "abc12345678", "abc12345679", "abc12345680"],
        "transaction_time": [
            {"seconds": 1661967000, "nanos": 335616980},
            {"seconds": 1661967010, "nanos": 335616988},
            {"seconds": 1661967145, "nanos": 335616980},
            {"seconds": 1661967300, "nanos": 335616989}
        ],
        "owner": ["0.0.45", "0.0.45", "0.0.45", "0.0.45", ],
        "price": [None, 2020, 4522, 100, ]
    })
    geocoder = geo.GeoCoder()

    def test_valid_details(self):
        result = nft.transform_details(self.details, self.geocoder)

        assert result['nft_id'] == self.details.nft_id
        assert result['current_owner'] == '0.0.45'
        # current time - first transaction time as days
        expected_days = int((time.time_ns() - (1661967000 * nft.NANOSECONDS_PER_SECOND)) / nft.NANOSECONDS_PER_DAY)
        assert result['nft_age'] == expected_days
        assert result['num_owners'] == 1
        assert result['avg_price'] == 0
        assert result['last_price'] == 0
        assert result['num_price_chg'] == 2
        assert result['nft_state'] == 'LISTED'
        assert result['latitude'] == pytest.approx(38.319047, rel=1e-6)
        assert result['longitude'] == pytest.approx(-92.498918, rel=1e-6)


class TestRecordsToList:
    def test_valid_records(self):
        records = [{'a': 'b', 'foo': 'bar'}, {'a': 'c', 'foo': 'baz'}]
        record_of_lists = nft.records_to_list(records)

        assert record_of_lists['a'] == ['b', 'c']
        assert record_of_lists['foo'] == ['bar', 'baz']


class TestNftTransformedResponse:
    def test_valid(self):
        response = nft.NftTransformedResponse.parse_obj({
            'nft_id': [{'token_id': "0.0.3", "serial_number": 7}],
            'current_owner': ["0.0.3"],
            'nft_age': [8],
            'num_owners': [1],
            'avg_price': [100.30],
            'last_price': [100],
            'num_price_chg': [1],
            'nft_state': ['LISTED'],
            'latitude': [12.34],
            'longitude': [56.78],
        })

        assert response.nft_state == ['LISTED']

    def test_mismatched_length(self):
        with pytest.raises(ValidationError, match='Lists must all be the same length!'):
            nft.NftTransformedResponse.parse_obj({
                'nft_id': [{'token_id': "0.0.3", "serial_number": 7}],
                'current_owner': ["0.0.3", "0.0.5"],
                'nft_age': [8, 9, 10],
                'num_owners': [],
                'avg_price': [100.30],
                'last_price': [100],
                'num_price_chg': [1],
                'nft_state': ['LISTED'],
                'latitude': [12.34],
                'longitude': [56.78],
            })
