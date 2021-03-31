from unittest import mock

import pytest

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestCalendarService:
    @mock.patch('requests.get')
    def test_authorize_success(self, mocked_get, test_client):
        mocked_get.return_value.json.return_value = {}
        response = test_client.get('/rest/api/v1/authorization/calendar-service')

        assert response.status_code == 200


class TestCalendarServiceCallback:
    @mock.patch('requests.get')
    def test_callback_success(self, mocked_get, test_client):
        mocked_get.return_value.json.return_value = {}
        response = test_client.get(
            '/rest/api/v1/authorization/calendar-service/oauth2callback'
        )

        assert response.status_code == 200


class TestCalendarServiceRevoke:
    @mock.patch('requests.get')
    def test_revoke_success(self, mocked_get, test_client):
        mocked_get.return_value.json.return_value = {}
        response = test_client.get('/rest/api/v1/authorization/calendar-service/revoke')

        assert response.status_code == 200


class TestCalendarServiceClear:
    @mock.patch('requests.get')
    def test_clear_success(self, mocked_get, test_client):
        mocked_get.return_value.json.return_value = {}
        response = test_client.get('/rest/api/v1/authorization/calendar-service/clear')

        assert response.status_code == 200


class TestSpotifyService:
    @mock.patch('requests.get')
    def test_authorize_success(self, mocked_get, test_client):
        mocked_get.return_value.json.return_value = {}
        response = test_client.get('/rest/api/v1/authorization/spotify-service')

        assert response.status_code == 200


class TestSpotifyServiceCallback:
    @mock.patch('requests.get')
    def test_callback_success(self, mocked_get, test_client):
        mocked_get.return_value.json.return_value = {}
        response = test_client.get(
            '/rest/api/v1/authorization/spotify-service/oauth2callback'
        )

        assert response.status_code == 200
