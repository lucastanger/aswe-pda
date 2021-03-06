import requests


class SpotifyService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://localhost:5565/rest/api/v1'

    def query(self):
        requests.get('{}/spotify/auth'.format(self.base_url))

        artist_img = []
        artist_name = []
        track_img = []
        track_name = []

        try:
            artists, tracks = self.get_recap()
            for item_a, item_t in artists['items'], tracks['items']:
                artist_img.append(item_a['images'][0]['url'])
                artist_name.append(item_a['name'])

                track_img.append(item_t['images'][0]['url'])
                track_name.append(item_t['name'])
        except Exception as inst:
            print(inst)
            return 'Invalid response!'

        print('Erfolgreich')
        recap_artist = [artist_img, artist_name]
        recap_tracks = [track_img, track_name]

        return recap_artist, recap_tracks

    def authenticate(self):
        requests.get(f'{self.base_url}/spotify/auth')

    def get_recap(self):
        artists = requests.get(f'{self.base_url}/spotify/profile/artists')
        tracks = requests.get(f'{self.base_url}/spotify/profile/tracks')
        return artists.json(), tracks.json()


service = SpotifyService()
print(service.query())
