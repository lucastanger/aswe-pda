import requests

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
SPOTIFY_API_URL = '{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)

USER_PROFILE_ENDPOINT = '{}/{}'.format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = '{}/{}'.format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = '{}/{}'.format(
    USER_PROFILE_ENDPOINT, 'top'
)  # /<type>
USER_RECENTLY_PLAYED_ENDPOINT = '{}/{}/{}'.format(
    USER_PROFILE_ENDPOINT, 'player', 'recently-played'
)
BROWSE_FEATURED_PLAYLISTS = '{}/{}/{}'.format(
    SPOTIFY_API_URL, 'browse', 'featured-playlists'
)
START_STOP_MUSIC_ENDPOINT = '{}/{}'.format(USER_PROFILE_ENDPOINT, 'player')

ARTIST_IMAGE_URL = '{}/{}'.format(SPOTIFY_API_URL, 'artists')


def get_user_profile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_user_playlists(auth_header):
    url = USER_PLAYLISTS_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_user_top(auth_header, t):
    if t not in ['artists', 'tracks']:
        return None
    url = '{}/{type}?time_range=long_term'.format(
        USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT, type=t
    )
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_user_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_featured_playlists(auth_header):
    url = BROWSE_FEATURED_PLAYLISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def start_music(auth_header):
    url = '{}/{}'.format(START_STOP_MUSIC_ENDPOINT, 'play')
    resp = requests.put(url, headers=auth_header)
    return resp.ok


def pause_music(auth_header):
    url = '{}/{}'.format(START_STOP_MUSIC_ENDPOINT, 'pause')
    resp = requests.put(url, headers=auth_header)
    return resp.ok


def get_image_url(auth_header, a_id):
    url = '{}/{}'.format(ARTIST_IMAGE_URL, a_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()
