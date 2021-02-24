import requests

SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "me")
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, "playlists")
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(
    USER_PROFILE_ENDPOINT, "top"
)  # /<type>
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(
    USER_PROFILE_ENDPOINT, "player", "recently-played"
)
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(
    SPOTIFY_API_URL, "browse", "featured-playlists"
)


def getUserProfile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def getUserPlaylists(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def getUserTop(auth_header, t):
    if t not in ["artists", "tracks"]:
        print("invalid type")
        return None
    url = "{}/{type}".format(USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT, type=t)
    resp = requests.get(url, headers=auth_header)
    print(resp)


def getUserRecentlyPlayed(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def getFeaturedPlaylists(auth_header):
    url = BROWSE_FEATURED_PLAYLISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()
