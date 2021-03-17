import requests
from dotmap import DotMap
from flask import make_response
import json


class SpotifyService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://spotify-service:5565/rest/api/v1'

    def query(self):
        if self.parameters['spotify-request'] == 'info':
            info = self.get_info()
            if info:
                return info
            return {'error': 'Could not receive a response'}
        elif self.parameters['spotify-request'] == 'playlist':
            playlist = self.get_playlist()
            if playlist:
                return playlist
            return {'error': 'Could not receive a response'}
        elif self.parameters['spotify-request'] == 'artists':
            artists = self.get_artists()
            if artists:
                return artists
            return {'error': 'Could not receive a response'}
        elif self.parameters['spotify-request'] == 'tracks':
            tracks = self.get_tracks()
            if tracks:
                return tracks
            return {'error': 'Could not receive a response'}
        elif self.parameters['spotify-request'] == 'recent':
            recent = self.get_recent()
            if recent:
                return recent
            return {'error': 'Could not receive a response'}
        elif self.parameters['spotify-request'] == 'featured':
            featured = self.get_featured()
            if featured:
                return featured
            return {'error': 'Could not receive a response'}
        elif self.parameters['spotify-request'] == 'play':
            play = self.play_music()
            if play:
                return {'message': 'Music is playing'}
            return {'error': 'Could not start the music'}
        elif self.parameters['spotify-request'] == 'pause':
            pause = self.pause_music()
            if pause:
                return {'message': 'Music is paused'}
            return {'error': 'Could not pause music'}

        return {'error': 'Invalid type'}

    def get_info(self):

        response = requests.get(f'{self.base_url}/spotify/profile/info')

        new_json = response.json()
        info = DotMap(new_json)
        result = []

        if response:
            result.append(
                {'name': info.display_name, 'url': info.external_urls.spotify, 'image': info.images[0].url}
            )
            return result
        return False

    def get_playlist(self):

        response = requests.get(f'{self.base_url}/spotify/profile/playlist')

        new_json = response.json()
        playlist = DotMap(new_json)
        result = []

        if response:
            for value in playlist['items']:
                result.append(
                    {'name': value.name, 'image': value.images[0].url, 'url': value.external_urls.spotify}
                )
            return result
        return False

    def get_artists(self):

        response = requests.get(f'{self.base_url}/spotify/profile/artists')

        new_json = response.json()
        artists = DotMap(new_json)
        result = []

        if response:
            for value in artists['items']:
                result.append(
                    {'name': value.name, 'image': value.images[0].url}
                )
            return result
        return False

    def get_tracks(self):

        response = requests.get(f'{self.base_url}/spotify/profile/tracks')

        new_json = response.json()
        tracks = DotMap(new_json)
        result = []

        if response:
            for value in tracks['items']:
                result.append(
                    {'name': value.name, 'image': value.album.images[0].url, 'artist': value.artists[0].name}
                )
            return result
        return False

    def get_recent(self):

        response = requests.get(f'{self.base_url}/spotify/profile/recent')

        new_json = response.json()
        recent = DotMap(new_json)
        result = []

        if response:
            for value in recent['items']:
                result.append(
                    {'tracks': value.track.name, 'artist': value.track.artists[0].name}
                )
            return result
        return False

    def get_featured(self):

        response = requests.get(f'{self.base_url}/spotify/profile/featured')

        new_json = response.json()
        featured = DotMap(new_json)
        result = []

        result.append({'message': featured.message})

        if response:
            for value in featured.playlists['items']:
                result.append(
                    {'name': value.name, 'image': value.images[0].url}
                )
            return result
        return False

    def play_music(self):
        response = requests.get(f'{self.base_url}/spotify/play')
        return response

    def pause_music(self):
        response = requests.get(f'{self.base_url}/spotify/pause')
        return response
