import requests
from flask import make_response


class SpotifyService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://spotify-service:5565/rest/api/v1'

    def query(self):

        type = self.parameters['type']

        artist_img = []
        artist_name = []
        track_img = []
        track_name = []

        if type == 'recent':
            artists, tracks = self.get_recap()
        else:
            return make_response({'error': 'Invalid type'}, 401)

        for item_a, item_t in artists['items'], tracks['items']:
            artist_img.append(item_a['images'][0]['url'])
            artist_name.append(item_a['name'])

            track_img.append(item_t['images'][0]['url'])
            track_name.append(item_t['name'])

        recap_artist = [artist_img, artist_name]
        recap_tracks = [track_img, track_name]

        return recap_artist, recap_tracks

    def get_recap(self):
        artists = requests.get(f'{self.base_url}/spotify/profile/artists')
        tracks = requests.get(f'{self.base_url}/spotify/profile/tracks')
        return artists.json(), tracks.json()


service = SpotifyService()
print(service.query())
