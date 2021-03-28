from unittest import mock
from unittest.mock import MagicMock

import pytest

from app import app


@pytest.fixture()
def test_client(mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value={
            '_id': '1234',
            'general': {},
            'dualis': {},
            'news': {},
            'weather': {},
            'stocks': {}
    })
    mocker.patch('pymongo.collection.Collection.replace_one', return_value=None)
    return app.test_client()


class TestConfigurationService:
    def test_get_configuration_success(self, test_client):
        response = test_client.get('/rest/api/v1/configuration/')

        assert response.status_code == 200

    def test_post_configuration_success(self, test_client):
        response = test_client.post('/rest/api/v1/configuration/', json={
            'general': {},
            'dualis': {},
            'news': {},
            'weather': {},
            'stocks': {},
        })

        assert response.status_code == 200


class TestStockService:
    @mock.patch('src.services.CalendarService.query', return_value={})
    def test_query_success(self, mocked_query, test_client):
        response = test_client.post('/rest/api/v1/dialogflow/query', json={'message': 'agenda'})

        assert mocked_query.called
        assert response.status_code == 200
