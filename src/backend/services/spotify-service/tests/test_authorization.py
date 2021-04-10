from unittest import mock
from requests.models import Response

import pytest

from app import app

test_response = Response()
test_response._content = b'{"access_token": "testToken", "refresh_token": "testRefreshToken"}'


@pytest.fixture()
def test_client(mocker):
    mocker.patch('src.flask_spotify_auth.requests.post', return_value=test_response)
    mocker.patch('src.flask_spotify_auth.MongoDB', return_value=None)
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
