from fastapi.testclient import TestClient
import time
from services.nft_transformer.main import app, API_PREFIX, nft

client = TestClient(app)

TWO_MINUTES_IN_NANOSECONDS = 120000000000.0

# MINTED_NFT = {
#     "msg_type": "MINTED",
#     "asset_id": "9DEFC49A.D0A4.4BED866F.6D083A-1E1BE8-560984084",
#     "minting_owner": "9DEFC49A.D0A4.4BED866F",
#     "minting_time": 1648788141000000000,  # 2022-04-01T04:42:21Z as nanoseconds since epoch
#     "transaction_id": "94F5-7CB4D0DFB04C",
#     "transaction_memo": "Von der Lebendigen Erde gGmbH verifizierte CO2-Ausgleiche.",
#     "project_category": "FOREST_CONSERV",
#     "project_type": "EFF_REFOR",
#     "country": "CMR",
#     "first_subdivision": "CM-SW",
#     "device_id": "CBB84414-862A-5BCD516FC635",
#     "guardian_id": "7227-4CD0-B164-0E8A-106E-1510"
# }


class TestTransformer:
    valid_data = [
        {
            "nft_id": {"token_id": "1.2.3", "serial_number": 1},
            "msg_type": ["LISTED", "LISTED", "LISTED", ],
            "country": "USA",
            "first_subdivision": "MO",
            "minting_time": 1661400288,
            "transaction_id": ["abc12345678", "abc12345679", "abc12345680"],
            "transaction_time": [
                {"seconds": 1661967010, "nanos": 335616988},
                {"seconds": 1661967145, "nanos": 335616980},
                {"seconds": 1661967300, "nanos": 335616989},
            ],
            "owner": ["0.0.45", "0.0.45", "0.0.45"],
            "price": [2020, 4522, 100]
        },
        {
            "nft_id": {"token_id": "1.2.3", "serial_number": 2},
            "msg_type": ["LISTED", "LISTED", "LISTED"],
            "country": "USA",
            "first_subdivision": "MO",
            "minting_time": 1661400288,
            "transaction_id": ["abc12345678", "abc12345679", "abc12345680"],
            "transaction_time": [
                {"seconds": 1661967010, "nanos": 335616988},
                {"seconds": 1661967145, "nanos": 335616980},
                {"seconds": 1661967300, "nanos": 335616989},
            ],
            "owner": ["0.0.44", "0.0.45", "0.0.46"],
            "price": [2120, 4622, 300]
        },
    ]

    def test_no_errors_single_nft(self):
        response = client.post(
            f'{API_PREFIX}/data_transformer',
            json=[self.valid_data[0]]
        )
        assert response.status_code == 200
        body = response.json()
        assert body['nft_id'] == [{"token_id": "1.2.3", "serial_number": 1}]
        assert body['last_price'] == [0]
        assert body['current_owner'] == ["0.0.45"]

        # Current timestamp - first transaction as days
        expected_days = int((time.time_ns() - (1661967010 * nft.NANOSECONDS_PER_SECOND)) / nft.NANOSECONDS_PER_DAY)
        assert body['nft_age'] == [expected_days]

    def test_no_errors_multiple_nft(self):
        response = client.post(
            f'{API_PREFIX}/data_transformer',
            json=self.valid_data
        )
        assert response.status_code == 200
        body = response.json()
        assert body['nft_id'] == [
            {"token_id": "1.2.3", "serial_number": 1},
            {"token_id": "1.2.3", "serial_number": 2},
        ]
        assert body['last_price'] == [0, 0]
        assert body['current_owner'] == ["0.0.45", "0.0.46"]

    def test_mismatch_lengths(self):
        data = self.valid_data.copy()
        data[0]['price'] = [100]  # change from 3 elements to 1
        response = client.post(
            f'{API_PREFIX}/data_transformer',
            json=data
        )
        body = response.json()
        assert response.status_code == 422
        assert body['error']['code'] == 1006
        assert body['error']['detail'][0]['msg'] == 'Lists must all be the same length!'
        # make sure it's the root validator that failed
        assert body['error']['detail'][0]['loc'] == ['body', 0, '__root__']


class TestPricingTransforms:
    purchased_data = [{
        "nft_id": {"token_id": "1.2.3", "serial_number": 3},
        "msg_type": [
            nft.MessageType.MINTED,
            nft.MessageType.LISTED,
            nft.MessageType.PURCHASED,
            nft.MessageType.LISTED,
            nft.MessageType.PURCHASED,
            nft.MessageType.LISTED,
        ],
        "country": "USA",
        "first_subdivision": "MO",
        "minting_time": 1661400288,
        "transaction_id": [
            "abc12345678",
            "abc23456781",
            "abc34567812",
            "abc45678123",
            "abc56781234",
            "abc67812345",
        ],
        "transaction_time": [
            {"seconds": 1661967010, "nanos": 335616988},  # MINTED
            {"seconds": 1661967145, "nanos": 335616980},  # LISTED
            {"seconds": 1661967300, "nanos": 335616989},  # PURCHASED
            {"seconds": 1662267010, "nanos": 335616988},  # LISTED
            {"seconds": 1662267145, "nanos": 335616988},  # PURCHASED
            {"seconds": 1662267300, "nanos": 335616988},  # LISTED
        ],
        "owner": ["0.0.45", "0.0.45", "0.0.55", "0.0.55", "0.0.60", "0.0.60"],
        "price": [0, 2000, 2000, 4051, 4001, 6000]
    }]

    def test_price_features(self):
        response = client.post(f'{API_PREFIX}/data_transformer', json=self.purchased_data)
        body = response.json()
        assert body['nft_state'] == [nft.MessageType.LISTED]
        assert body['last_price'] == [4001]  # last *purchased* price
        assert body['avg_price'] == [int((2000 + 4001) / 2)]  # only *purchased* prices
        # Change of value between any pairwise sequence of listed or purchased.
        # The first change from MINTED 0 to LISTED n, does not count as a change.
        assert body['num_price_chg'] == [3]

        # expected = current time - first transaction time as days
        expected_days = int((time.time_ns() - (1661967010 * nft.NANOSECONDS_PER_SECOND)) / nft.NANOSECONDS_PER_DAY)
        assert body['nft_age'] == [expected_days]
