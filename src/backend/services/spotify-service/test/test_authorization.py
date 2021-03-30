from unittest import mock

import pytest

from app import app


@pytest.fixture()
def test_client(mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=None)
    mocker.patch('pymongo.collection.Collection.replace_one', return_value=None)
    return app.test_client()


class TestAuthorization:
    def test_authorization_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/auth', follow_redirects=True)

        assert response.status_code == 200


class TestCallback:
    def test_callback_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/callback')

        assert response.status_code == 201
