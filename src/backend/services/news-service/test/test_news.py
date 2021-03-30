import pytest

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestNews:
    def test_top_news_success(self, test_client):
        response = test_client.get('/rest/api/v1/news/top').json()

        assert response['status'] == 'ok'

    def test_everything_news_success(self, test_client):
        response = test_client.get('rest/api/v1/news/everything?source=abc-news').json()

        assert response['status'] == 'ok'

    def test_everything_news_failure(self, test_client):
        response = test_client.get('rest/api/v1/news/everything?source=notASource').json()

        assert response['status'] == 'error'

    def test_everything_news_search_success(self, test_client):
        response = test_client.get('rest/api/v1/news/everything/search?source=abc-news&keyWord=testKeyWord').json()

        assert response['status'] == 'ok'

    def test_everything_news_search_failure(self, test_client):
        response = test_client.get('rest/api/v1/news/everything/search?source=notASource&keyWord=testKeyWord').json()

        assert response['status'] == 'error'

    def test_sources_success(self, test_client):
        response = test_client.get('/rest/api/v1/news/sources').json()

        assert response['status'] == 'ok'
