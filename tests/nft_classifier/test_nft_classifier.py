from fastapi.testclient import TestClient

from services.nft_classifier.main import app, API_PREFIX, POOL

client = TestClient(app)


class TestNftClassifier:
    def test_empty_nft(self):
        response = client.post(
            f'{API_PREFIX}/{POOL}',
            headers={"Content-Type": "application/json"},
            json={
                "nft_id": [],
                "transaction_id": [],
                "transaction_time": [],
                "minting_owner": [],
                "owner": [],
                "country": [],
                "first_subdivision": [],
                "latitude": [],
                "longitude": [],
                "project_category": [],
                "project_type": [],
                "vintage_year": [],
                "nft_age": [],
                "num_owners": [],
                "avg_price": [],
                "last_price": [],
                "num_price_chg": [],
                "nft_state": []
            }
        )
        assert response.status_code == 422  # Unprocessable Entity

    def test_single_nft(self):
        response = client.post(
            f'{API_PREFIX}/{POOL}',
            headers={"Content-Type": "application/json"},
            json={
                "nft_id": [{"token_id": "0.0.9401", "serial_number": 1}],
                "transaction_id": ["0.0.9401@1602138343.335616988"],
                "transaction_time": [{"seconds": 1566015267, "nanos": 335616988}],
                "minting_owner": ["0.0.9401"],
                "owner": ["0.0.9401"],
                "country": ["CHN"],
                "first_subdivision": ["GD"],
                "latitude": [23.1357694],
                "longitude": [113.1982688],
                "project_category": ["RENEW_ENERGY"],
                "project_type": ["SOLAR"],
                "vintage_year": [2020],
                "nft_age": [2],
                "num_owners": [1],
                "avg_price": [7500],
                "last_price": [10000],
                "num_price_chg": [2],
                "nft_state": ["LISTED"]
            }
        )
        assert response.status_code == 200
        assert response.json()['nft_id'] == [{"token_id": "0.0.9401", "serial_number": 1}]
        assert response.json()['transaction_id'] == ['0.0.9401@1602138343.335616988']
        assert response.json()['transaction_time'] == [{"seconds": 1566015267, "nanos": 335616988}]
        assert response.json()['token_pool_id'] == ['272986af-24ea-4473-a4a3-99acb70128c5']
        assert response.json()['name_pool'] == [
            'GTM_KHM_KEN_BGR_GBR_IND_IDN_PER_RWA_FRA_HND_ETH_NIC_MMR_GIN_MOZ_USA_RENEW_ENERGY_SOLAR_272986af-24ea-4473-a4a3-99acb70128c5']
        assert response.json()['pooling_version'] == ['0.0.0.0']

    def test_multi_nft(self):
        response = client.post(
            f'{API_PREFIX}/{POOL}',
            headers={"Content-Type": "application/json"},
            json={
                "nft_id": [{"token_id": "0.0.9401", "serial_number": 1}, {"token_id": "0.0.9401", "serial_number": 2}],
                "transaction_id": ["0.0.9401@1602138343.335616988", "0.0.9401@1602138344.335616988"],
                "transaction_time": [{"seconds": 1566015267, "nanos": 000000000}, {"seconds": 1566015267, "nanos": 000000000}],
                "minting_owner": ["0.0.9401", "0.0.9401"],
                "owner": ["0.0.9401", "0.0.100"],
                "country": ["CHN", "USA"],
                "first_subdivision": ["GD", "MO"],
                "latitude": [23.1357694, 38.7604815],
                "longitude": [113.1982688, -92.5617875],
                "project_category": ["RENEW_ENERGY", "FOREST_CONSERV"],
                "project_type": ["SOLAR", "EFF_REFOR"],
                "vintage_year": [2020, 2018],
                "nft_age": [2, 4],
                "num_owners": [1, 2],
                "avg_price": [0, 422222],
                "last_price": [10000, 422222],
                "num_price_chg": [2, 4],
                "nft_state": ["LISTED", "RESOLD"]
            }
        )
        assert response.status_code == 200
        assert response.json()['nft_id'] == [{"token_id": "0.0.9401", "serial_number": 1}, {
            "token_id": "0.0.9401", "serial_number": 2}]
        assert response.json()['transaction_id'] == ['0.0.9401@1602138343.335616988', '0.0.9401@1602138344.335616988']
        assert response.json()['transaction_time'] == [{"seconds": 1566015267, "nanos": 000000000}, {
            "seconds": 1566015267, "nanos": 000000000}]
        assert response.json()['token_pool_id'] == [
            '272986af-24ea-4473-a4a3-99acb70128c5',
            'a3cd8341-1174-46f1-809e-570ba64b38cf']
        assert response.json()['name_pool'] == [
            'GTM_KHM_KEN_BGR_GBR_IND_IDN_PER_RWA_FRA_HND_ETH_NIC_MMR_GIN_MOZ_USA_RENEW_ENERGY_SOLAR_272986af-24ea-4473-a4a3-99acb70128c5',
            'MMR_IDN_KEN_USA_GTM_KHM_HND_MOZ_PER_BGR_NIC_GBR_GIN_IND_FRA_ETH_RWA_COMM_ENRGY_EFF_COOK_STV_a3cd8341-1174-46f1-809e-570ba64b38cf']
        assert response.json()['pooling_version'] == ['0.0.0.0', '0.0.0.0']
