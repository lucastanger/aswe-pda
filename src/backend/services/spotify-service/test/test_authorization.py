from unittest import mock

import pytest

from app import app


@pytest.fixture()
def test_client(mocker):
    mocker.patch('src/backend/services/spotify-service/src/flask_spotify_auth.authorize', return_value=True)
    return app.test_client()


class TestAuthorization:
    def test_authorization_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/auth')

        assert response.status_code == 200


class TestCallback:
    __code = 'testCode'

    def test_callback_success(self, test_client):
        response = test_client.get(f'/rest/api/v1/spotify/callback?code={self.__code}')

        assert response.status_code == 200
