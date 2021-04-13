from unittest import mock

import pytest

from src.services.news_service import NewsService

BASE_URL = 'http://news-service:5575/rest/api/v1'
PAPER_ID = 'abc-news'
CATEGORY = 'sports'


@pytest.fixture
def service(mocker, parameters):
    mocker.patch(
        'src.backend.middleware.src.services.news_service.NewsService.get_db_info',
        paper_id=PAPER_ID,
        category=CATEGORY,
    )
    news_service = NewsService(parameters)
    return news_service


class TestNewsService:
    __type_top = 'top'
    __type_everything = 'everything'
    __type_sources = 'sources'
    __search = 'someKeyWord'

    @mock.patch('request.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_top}])
    def test_top_news_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(
            f'{BASE_URL}/news/{self.__type_top}/category?category={CATEGORY}'
        )

    @mock.patch('request.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_everything}])
    def test_everything_news_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(
            f'{BASE_URL}/news/{self.__type_everything}?source={PAPER_ID}'
        )

    @mock.patch('request.get')
    @pytest.mark.parametrize(
        'parameters', [{'type': __type_everything, 'search': __search}]
    )
    def test_everything_search_news_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(
            f'{BASE_URL}/news/{self.__type_everything}/search?keyWord={self.__search}&source={PAPER_ID}'
        )

    @mock.patch('request.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_sources}])
    def test_sources_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_sources}')
