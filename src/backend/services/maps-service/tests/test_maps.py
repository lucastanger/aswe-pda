import pytest

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestMaps:
    def test_route_success(self, test_client):
        response = test_client.get(
            '/rest/api/v1/maps/route?'
            'origin=Disneyland&'
            'destination=Universal+Studios+Hollywood&'
            'arrival_time=2021-03-26T12:00:00+01:00'
        )

        assert response.status_code == 200

    def test_route_success_missing_arrival_time(self, test_client):
        response = test_client.get(
            '/rest/api/v1/maps/route?'
            'origin=Disneyland&'
            'destination=Universal+Studios+Hollywood'
        )

        assert response.status_code == 200

    def test_route_fail_missing_parameters(self, test_client):
        response = test_client.get(
            '/rest/api/v1/maps/route'
        )

        assert response.status_code == 400
