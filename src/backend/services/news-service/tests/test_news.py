import pytest
import json

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestNews:
    def test_top_news_success(self, test_client):
        response = test_client.get('/rest/api/v1/news/top')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['status'] == 'ok'

    def test_everything_news_success(self, test_client):
        response = test_client.get('/rest/api/v1/news/everything?source=abc-news')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['status'] == 'ok'

    def test_everything_news_failure(self, test_client):
        response = test_client.get('/rest/api/v1/news/everything?source=notASource')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['status'] == 'error'

    def test_everything_news_search_success(self, test_client):
        response = test_client.get(
            '/rest/api/v1/news/everything/search?source=abc-news&keyWord=testKeyWord'
        )
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['status'] == 'ok'

    def test_everything_news_search_failure(self, test_client):
        response = test_client.get(
            '/rest/api/v1/news/everything/search?source=notASource&keyWord=testKeyWord'
        )
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['status'] == 'error'

    def test_sources_success(self, test_client):
        response = test_client.get('/rest/api/v1/news/sources')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['status'] == 'ok'
