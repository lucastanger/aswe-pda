import requests
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
                return make_response(info, 200)
            return make_response({'error': 'Could not receive a response'}, 402)
        elif self.parameters['spotify-request'] == 'playlist':
            playlist = self.get_playlist()
            if playlist:
                return make_response(playlist, 200)
            return make_response({'error': 'Could not receive a response'}, 402)
        elif self.parameters['spotify-request'] == 'artists':
            artists = self.get_artists()
            if artists:
                return make_response(artists, 200)
            return make_response({'error': 'Could not receive a response'}, 402)
        elif self.parameters['spotify-request'] == 'tracks':
            tracks = self.get_tracks()
            if tracks:
                return make_response(tracks, 200)
            return make_response({'error': 'Could not receive a response'}, 402)
        elif self.parameters['spotify-request'] == 'recent':
            recent = self.get_recent()
            if recent:
                return make_response(recent, 200)
            return make_response({'error': 'Could not receive a response'}, 402)
        elif self.parameters['spotify-request'] == 'featured':
            featured = self.get_featured()
            if featured:
                return make_response(featured, 200)
            return make_response({'error': 'Could not receive a response'}, 402)
        elif self.parameters['spotify-request'] == 'play':
            play = self.play_music()
            if play:
                return make_response({'message': 'Music is playing'}, 200)
            return make_response({'error': 'Could not start the music'}, 403)
        elif self.parameters['spotify-request'] == 'pause':
            pause = self.pause_music()
            if pause:
                return make_response({'message': 'Music is paused'}, 200)
            return make_response({'error': 'Could not pause music'}, 403)

        return make_response({'error': 'Invalid type'}, 401)

    def get_info(self):

        response_json = requests.get(f'{self.base_url}/spotify/profile/info').json()

        if response_json:
            info_name = response_json['display_name']
            info_email = response_json['email']
            info_url = response_json['external_urls']['spotify']
            info_image = response_json['images'][0]['url']

            info = json.dumps({'info': {
                'name': info_name,
                'email': info_email,
                'url': info_url,
                'image': info_image
            }})

            return info
        return False

    def get_playlist(self):

        response_json = requests.get(f'{self.base_url}/spotify/profile').json()

        if response_json:
            index = 0

            z = json.loads('{"playlists": []}')

            for item in response_json['items']:
                z['playlists'][index] = {
                    'name': item['name'],
                    'image': item['images'][0]['url'],
                    'url': item['external_urls']['spotify']
                }
                index += 1

            return json.dumps(z)
        return False

    def get_artists(self):

        response_json = requests.get(f'{self.base_url}/spotify/profile/artists').json()

        if response_json:
            index = 0

            z = json.loads('{"artists": []}')

            for item in response_json['items']:
                z['artists'][index] = {
                    'name': item['name'],
                    'image': item['images'][0]['url']
                }

                index += 1

            return json.dumps(z)
        return False

    def get_tracks(self):

        response_json = requests.get(f'{self.base_url}/spotify/profile/tracks').json()

        if response_json:
            index = 0

            z = json.loads('{"tracks": []}')

            for item in response_json['tracks']:
                z['tracks'][index] = {
                    'name': item['name'],
                    'image': item['album']['images'][0]['url'],
                    'artist': item['artists'][0]['name']
                }

                index += 1

            return json.dumps(z)
        return False

    def get_recent(self):

        response_json = requests.get(f'{self.base_url}/spotify/profile/recent').json()

        if response_json:
            index = 0

            z = json.loads('{"recent": []}')

            for item in response_json['items']:
                z['recent'][index] = {
                    'track': item['track']['name'],
                    'artist': item['track']['artists'][0]['name']
                }

                index += 1

            return json.dumps(z)
        return False

    def get_featured(self):

        response_json = requests.get(f'{self.base_url}/spotify/profile/featured').json()

        if response_json:
            index = 0

            z = json.loads('{"featured": [], "message": ""}')

            z['message'] = response_json['message']

            for item in response_json['playlists']:
                for i in item['items']:
                    z['featured'] = {
                        'name': i['name'],
                        'image': i['images'][0]['url']
                    }

                    index += 1

            return json.dumps(z)
        return False

    def play_music(self):
        response = requests.get(f'{self.base_url}/spotify/play')
        return response

    def pause_music(self):
        response = requests.get(f'{self.base_url}/spotify/pause')
        return response
