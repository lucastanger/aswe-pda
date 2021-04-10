import json
from unittest import mock
from requests import Response

import pytest

from src.services.news_service import NewsService

BASE_URL = 'http://news-service:5575/rest/api/v1'
PAPER_ID = 'abc-news'
CATEGORY = ['sports']

test_response = Response()
test_response._content = b'{"sources": [{"name": "testName", "url": "testURL", "id": "testID"}], "articles": [{"title": "testTitle", "urlToImage": "testURLToImage", "url": "testURL"}]}'
test_response.status_code = 200

test_response_no_url = Response()
test_response_no_url._content = b'{"articles": [{"title": "testTitle", "url": "testURL"}]}'
test_response_no_url.status_code = 200


@pytest.fixture
def service_with_db_info(mocker, parameters):
    mocker.patch.object(NewsService, 'get_db_info', return_value=[PAPER_ID, CATEGORY])
    news_service = NewsService(parameters)
    return news_service


@pytest.fixture
def service_without_db_info(mocker, parameters):
    mocker.patch.object(NewsService, 'get_db_info', return_value=[None, None])
    news_service = NewsService(parameters)
    return news_service


class TestNewsService:
    __type_top = 'top'
    __type_everything = 'everything'
    __type_sources = 'sources'
    __search = 'someKeyWord'

    @mock.patch('requests.get', return_value=test_response_no_url)
    @pytest.mark.parametrize('parameters', [{'type': __type_top}])
    def test_top_news_category_success(self, mocked_get, service_with_db_info):
        _response = service_with_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_top}/category?category={CATEGORY[0]}')

        assert _response[0]['img'] == 'https://www.bag.admin.ch/bag/de/home/das-bag/aktuell/news/news-02-09-2020/_jcr_content/image.imagespooler.png/1603898250046/588.1000/Icons-18.png'

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'type': __type_top}])
    def test_top_news_success(self, mocked_get, service_without_db_info):
        _response = service_without_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_top}')

        assert _response[0]['title'] == 'testTitle'

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_everything}])
    def test_everything_news_success(self, mocked_get, service_without_db_info):
        _response = service_without_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_everything}')

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_everything}])
    def test_everything_news_paper_success(self, mocked_get, service_with_db_info):
        _response = service_with_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_everything}?source={PAPER_ID}')

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_everything, 'search': __search}])
    def test_everything_news_search_and_paper_success(self, mocked_get, service_with_db_info):
        _response = service_with_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_everything}/search?keyWord={self.__search}&source={PAPER_ID}')

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'type': __type_everything, 'search': __search}])
    def test_everything_news_search_success(self, mocked_get, service_without_db_info):
        _response = service_without_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_everything}')

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'type': __type_sources}])
    def test_sources_success(self, mocked_get, service_with_db_info):
        _response = service_with_db_info.query()

        mocked_get.assert_called_with(f'{BASE_URL}/news/{self.__type_sources}')

        assert _response[0]['name'] == 'testName'

    @pytest.mark.parametrize('parameters', [{'type': 'failureType'}, {'noType': 'noType'}])
    def test_news_failure(self, service_with_db_info):
        _response = service_with_db_info.query()

        assert _response == 'Please provide a valid type!' or _response == 'Please provide a type!'

