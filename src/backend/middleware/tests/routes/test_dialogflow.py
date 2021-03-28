from unittest import mock
from unittest.mock import MagicMock

import pytest

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestDialogflow:
    @mock.patch('src.services.CalendarService.query', return_value={})
    def test_query_success(self, mocked_query, test_client):
        response = test_client.post('/rest/api/v1/dialogflow/query', json={'message': 'agenda'})

        assert mocked_query.called
        assert response.status_code == 200
