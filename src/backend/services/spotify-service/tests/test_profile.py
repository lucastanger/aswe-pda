from unittest import mock

import pytest
import json

from app import app


@pytest.fixture()
def test_client(mocker):
    mocker.patch('src.flask_spotify_auth.get_auth_header', return_value=[None, True])
    mocker.patch('src.flask_spotify_auth.MongoDB', return_value=None)
    return app.test_client()


class TestProfile:
    # Check if the response is 401 - Unauthorized so we know the call was successful but
    # we did not provide a valid token since we dont authorize beforehand
    def test_profile_info_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/info')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401

    def test_profile_playlist_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/playlist')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401

    def test_profile_artists_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/artists')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401

    def test_profile_tracks_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/tracks')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401

    def test_profile_recent_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/recent')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401

    def test_profile_featured_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/featured')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401


class TestPlayPause:
    __artist_id = 'someID'

    def test_play_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/play')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error'] == 'Something went wrong or music already playing'

    def test_pause_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/pause')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error'] == 'Something went wrong or music already paused'

    def test_image_success(self, test_client):
        response = test_client.get(f'/rest/api/v1/spotify/image?id={self.__artist_id}')
        json_response = json.loads(response.get_data(as_text=True))

        assert json_response['error']['status'] == 401
