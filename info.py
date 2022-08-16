import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

SPOTIPY_CLIENT_ID = 'b6f2877e6a4946ee9739fe03ceeb9bf1'
SPOTIPY_CLIENT_SECRET = '636ee61020e54deba71b97d9ea299bdf'
SPOTIPY_REDIRECT_URI = 'https://www.youtube.com/'


scope = "user-library-read user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
tr = 'long_term'


from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])



#finds top songs depending on the time range. returns thme in a list
def findTopSongs():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_top_tracks(time_range=tr)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    i = 1
    l = []
    #Print Tracks and Calculate Popularity
    for track in tracks:
        l.append((i, track['artists'][0]['name'],track['name'], track['popularity']))
        i+=1


    return l

#finds top artists depending on the time range. returns them in a list
def findTopArtists():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    top_artists = sp.current_user_top_artists(time_range=tr)
    artists = top_artists['items']
    while top_artists['next']:
        top_artists = sp.next(top_artists)
        artists.extend(top_artists['items'])

    #Print top artists and average artist popularity
    j = 1
    l = []
    avg_artist_pop = 0
    for artist in artists:
        l.append((j, artist['name'], artist['popularity']))
        j+=1
    return l

#finds the dancability, energy, and valence of each song from user top tracks
#returns a list of songs 1-60 (position, song_name, dancability, energy, valence)
def findMood():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_top_tracks(time_range=tr)
    tracks = results['items']
    valences = []

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    i = 1
    for track in tracks:
        valences.append(track['uri'])
        i+=1

    dev = []

    mood_list = sp.audio_features(valences)
    #print(mood_list)
    for idx, m in enumerate(mood_list):
        dev.append((idx+1, sp.track(m['uri'])['name'], sp.track(m['uri'])['popularity'], m['danceability'], m['energy'], m['valence']))
    
    
    return dev

def findAvgSongPop(song_list):
    length = len(song_list)
    tot = 0
    for song in song_list:
        tot += song[3]
    return tot/length

def findAvgArtistPop(artist_list):
    length = len(artist_list)
    tot = 0
    for artist in artist_list:
        tot += artist[2]
    return tot/length



if __name__ == '__main__':
    pass
    #song_list = findTopSongs()
    # artist_list = findTopArtists()
    # mood = findMood()

    # for i in song_list:
    #     print(i)
    # print()
    # for i in artist_list:
    #     print(i)
    # print()
    # for i in mood:
    #     print(i)

    # print(findAvgSongPop(song_list))
    # print(findAvgArtistPop(artist_list))

