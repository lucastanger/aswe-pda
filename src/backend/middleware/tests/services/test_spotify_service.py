from unittest import mock
from requests.models import Response
import json

from unittest.mock import Mock

import pytest

from src.services.spotify_service import SpotifyService

BASE_URL = 'http://spotify-service:5565/rest/api/v1'


@pytest.fixture
def service(parameters):
    spotify_service = SpotifyService(parameters)
    return spotify_service


class TestSpotifyService:
    __info = 'info'
    __playlist = 'playlist'
    __artists = 'artists'
    __tracks = 'tracks'
    __recent = 'recent'
    __featured = 'featured'
    __play = 'play'
    __pause = 'pause'

    test_response = Response()
    test_response._content = b'{"images": [{"url": "testProfileURL"}], "display_name": "testDisplayName", "external_urls": {"spotify": "testSpotifyURL"}, "items": [{"images": [{"url": "testURL"}], "name": "testName", "external_urls": {"spotify": "testSpotifyURL"}, "album": {"images": [{"url": "testAlbumURL"}], "external_urls": {"spotify": "testSpotifyURL"}}, "artists": [{"name": "testArtistName"}]}]}'
    test_response.status_code = 200

    test_response_failure = Response()
    test_response_failure._content = b'{}'
    test_response_failure.status_code = 200

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'spotify-request': __info}])
    def test_spotify_info_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/profile/{self.__info}')

        assert _response[0]['name'] == 'testDisplayName'

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'spotify-request': __playlist}])
    def test_spotify_playlist_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/profile/{self.__playlist}')

        assert _response[0]['name'] == 'testName'

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'spotify-request': __artists}])
    def test_spotify_artists_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/profile/{self.__artists}')

        assert _response[0]['name'] == 'testName'

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'spotify-request': __tracks}])
    def test_spotify_tracks_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/profile/{self.__tracks}')

        assert _response[0]['name'] == 'testName'

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'spotify-request': __recent}])
    def test_spotify_recent_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/profile/{self.__recent}')

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'spotify-request': __featured}])
    def test_spotify_featured_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/profile/{self.__featured}')

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'spotify-request': __play}])
    def test_spotify_play_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/{self.__play}')

    @mock.patch('requests.get', return_value=test_response)
    @pytest.mark.parametrize('parameters', [{'spotify-request': __pause}])
    def test_spotify_pause_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/spotify/{self.__pause}')
