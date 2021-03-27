from unittest import mock

import pytest

from app import app
from src.routes.authorization import get_credentials


@pytest.fixture()
def test_client():
    return app.test_client()


class TestEvents:
    def test_date_success(self, test_client):
        response = test_client.get('/rest/api/v1/events/2021-03-26T12:00:00+01:00')

        assert response.status_code == 200

    def test_date_fail(self, test_client):
        response = test_client.get('/rest/api/v1/events/thisisnotadate')

        assert response.status_code == 400

    def test_date_today_success(self, test_client):
        response = test_client.get('/rest/api/v1/events/')

        assert response.status_code == 200
