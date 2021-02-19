import pytest

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestMaps:
    def test_maps_direction(self, test_client):
        response = test_client.get('/rest/api/v1/maps/direction?'
                                   'origin=Disneyland&'
                                   'destination=Universal+Studios+Hollywood&'
                                   'arrival_time=1613774210')

        assert response.status_code == 200
