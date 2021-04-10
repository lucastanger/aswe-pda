from unittest import mock
import pytest

from app import app


@pytest.fixture()
def test_client(mocker):
    mocker.patch('src/backend/services/spotify-service/src/flask_spotify_auth.get_auth_header', auth_header=None, success=True)
    return app.test_client()


class TestProfile:
    def test_profile_info_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/info')

        assert response['error']['status'] == 401

    def test_profile_playlist_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/playlist')

        assert response['error']['status'] == 401

    def test_profile_artists_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/artists')

        assert response['error']['status'] == 401

    def test_profile_tracks_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/tracks')

        assert response['error']['status'] == 401

    def test_profile_recent_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/recent')

        assert response['error']['status'] == 401

    def test_profile_featured_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/profile/featured')

        assert response['error']['status'] == 401


class TestPlayPause:
    __artist_id = 'someID'

    def test_play_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/play')

        assert response['error'] == 'Something went wrong or music already playing'

    def test_pause_success(self, test_client):
        response = test_client.get('/rest/api/v1/spotify/pause')

        assert response['error'] == 'Something went wrong or music already paused'

    def test_image_success(self, test_client):
        response = test_client.get(f'/rest/api/v1/spotify/image/{self.__artist_id}')

        assert response['error']['status'] == 401
