from unittest import mock

import pytest

from app import app
from unittest.mock import MagicMock


@pytest.fixture()
def test_client(mocker):
    mocker.patch('pymongo.collection.Collection.delete_many', return_value=None)
    mocker.patch('pymongo.collection.Collection.replace_one', return_value=None)
    mocker.patch('google_auth_oauthlib.flow.Flow.fetch_token', return_value=None)
    mocker.patch('google_auth_oauthlib.flow.Flow.credentials', return_value=None)
    return app.test_client()


class TestAuthorization:
    def test_authorize_success(self, test_client):
        response = test_client.get('/rest/api/v1/events/2021-03-26T12:00:00+01:00')

        assert response.status_code == 200


class TestCallback:
    def test_callback_success(self, test_client):
        response = test_client.get('/rest/api/v1/authorization/oauth2callback')

        assert response.status_code == 200


class TestRevoke:
    post_mock_success = MagicMock()
    post_mock_success.status_code = 200
    post_mock_fail = MagicMock()
    post_mock_fail.status_code = 400

    @mock.patch('requests.post', return_value=post_mock_success)
    def test_revoke_success(self, mocked_post, test_client):
        response = test_client.get('/rest/api/v1/authorization/revoke')

        assert response.status_code == 200

    @mock.patch('requests.post', return_value=post_mock_fail)
    def test_revoke_fail(self, mocked_post, test_client):
        response = test_client.get('/rest/api/v1/authorization/revoke')

        assert response.status_code == 400


class TestClear:
    def test_clear_success(self, test_client):
        response = test_client.get('/rest/api/v1/authorization/clear')

        assert response.status_code == 200
