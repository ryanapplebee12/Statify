import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os
import requests

#ryans branch
SPOTIPY_CLIENT_ID = 'b6f2877e6a4946ee9739fe03ceeb9bf1'
SPOTIPY_CLIENT_SECRET = '636ee61020e54deba71b97d9ea299bdf'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

SCOPE = "user-library-read user-top-read"


username = 'guest'

try:
    token = util.prompt_for_user_token(username, SCOPE, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
except:
    os.remove(".cache-" + username)
    token = util.prompt_for_user_token(username, SCOPE, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

# Creates Spotify Object
sp = spotipy.Spotify(auth=token)

results = sp.current_user_saved_tracks()
tracks = results['items']

while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

def get_genre(passed_track):
    # sp.artist returns an artist object
    artist = sp.artist(tracks["artists"][0]["external_urls"]["spotify"])
    genre = str(artist['genres'])
    return genre


for g in get_genre(tracks):
    print(g)