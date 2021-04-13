import requests
from dotmap import DotMap


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
            return play
        elif self.parameters['spotify-request'] == 'pause':
            pause = self.pause_music()
            return pause

        return {'error': 'Invalid type'}

    def get_info(self):

        response = requests.get(f'{self.base_url}/spotify/profile/info')

        new_json = response.json()
        info = DotMap(new_json)
        result = []

        if response:
            if len(info.images) > 0:
                result.append(
                    {
                        'name': info.display_name,
                        'url': info.external_urls.spotify,
                        'image': info.images[0].url,
                    }
                )
            else:
                result.append(
                    {
                        'name': info.display_name,
                        'url': info.external_urls.spotify,
                        'image': 'https://blog-recordjet-com.exactdn.com/wp-content/uploads/2014/10/spotify'
                        '-e1464103151339.jpg?strip=all&lossy=1&quality=92&ssl=1',
                    }
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
                if len(value.images) > 0:
                    result.append(
                        {
                            'name': value.name,
                            'image': value.images[0].url,
                            'url': value.external_urls.spotify,
                        }
                    )
                else:
                    result.append(
                        {
                            'name': value.name,
                            'image': 'https://blog-recordjet-com.exactdn.com/wp-content/uploads/2014/10/spotify'
                            '-e1464103151339.jpg?strip=all&lossy=1&quality=92&ssl=1',
                            'url': value.external_urls.spotify,
                        }
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
                if len(value.images) > 0:
                    result.append(
                        {
                            'name': value.name,
                            'image': value.images[0].url,
                            'url': value.external_urls.spotify,
                        }
                    )
                else:
                    result.append(
                        {
                            'name': value.name,
                            'image': 'https://blog-recordjet-com.exactdn.com/wp-content/uploads/2014/10/spotify'
                            '-e1464103151339.jpg?strip=all&lossy=1&quality=92&ssl=1',
                            'url': value.external_urls.spotify,
                        }
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
                if len(value.album.images) > 0:
                    result.append(
                        {
                            'name': value.name,
                            'image': value.album.images[0].url,
                            'artist': value.artists[0].name,
                            'url': value.album.external_urls.spotify,
                        }
                    )
                else:
                    result.append(
                        {
                            'name': value.name,
                            'image': 'https://blog-recordjet-com.exactdn.com/wp-content/uploads/2014/10/spotify'
                            '-e1464103151339.jpg?strip=all&lossy=1&quality=92&ssl=1',
                            'artist': value.artists[0].name,
                            'url': value.album.external_urls.spotify,
                        }
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
                param = {'id': value.track.artists[0].id}
                response_a = requests.get(
                    f'{self.base_url}/spotify/image', params=param
                )
                new_json_a = response_a.json()

                artist = DotMap(new_json_a)

                if len(artist.images) > 0:
                    result.append(
                        {
                            'tracks': value.track.name,
                            'artist': value.track.artists[0].name,
                            'image': artist.images[0].url,
                            'url': value.track.external_urls.spotify,
                        }
                    )
                else:
                    result.append(
                        {
                            'tracks': value.track.name,
                            'artist': value.track.artists[0].name,
                            'image': 'https://blog-recordjet-com.exactdn.com/wp-content/uploads/2014/10/spotify'
                            '-e1464103151339.jpg?strip=all&lossy=1&quality=92&ssl=1',
                            'url': value.track.external_urls.spotify,
                        }
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
                    {
                        'name': value.name,
                        'image': value.images[0].url,
                        'url': value.external_urls.spotify,
                    }
                )
            return result
        return False

    def play_music(self):
        response = requests.get(f'{self.base_url}/spotify/play')
        return response.json()

    def pause_music(self):
        response = requests.get(f'{self.base_url}/spotify/pause')
        return response.json()
