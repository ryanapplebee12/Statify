
from ast import Global
from asyncio import gather
import os
from flask import Flask, session, request, redirect, flash, render_template
from flask_session import Session
import spotipy
import uuid
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

USERNAME = 'poo'
SPOTIPY_CLIENT_ID = 'b6f2877e6a4946ee9739fe03ceeb9bf1'
SPOTIPY_CLIENT_SECRET = '636ee61020e54deba71b97d9ea299bdf'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/'
SCOPE = "user-library-read user-top-read"
TR = 'short_term'

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-top-read', 
                                                client_id= SPOTIPY_CLIENT_ID,
                                                client_secret= SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                                cache_handler=cache_handler, 
                                                show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        flash(auth_url)
        return render_template('index.html')

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    flash(spotify.me()["display_name"])
    return redirect('/page1')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    global TR
    TR = 'medium_term'
    return render_template('page3.html')

@app.route('/page4')
def page4():
    global TR
    TR = 'long_term'
    return render_template('page4.html')



#short term ##########################################
@app.route('/shortTermSongs')
def shortTermSongs():
    
    flash('These are your top songs. . .')
    flash('')
    l = findTopSongs()
    dev = findMood()
    for i in range(len(l)):
        line = l[i] + dev[i]
        flash(str(line[0]) + '  \t' + str(line[1]))
        #+ '\t\t' + str(line[2]) + '\t\t' + str(line[3]) + '\t' + str(line[4]) + '\t' + str(line[5]) + '\t' + str(line[6])
    flash('')
    flash('Your average song popularity is ' + str(round(findAvgSongPop(l), 2)))
    return render_template('shortTerm.html')

@app.route('/shortTermArtists')
def shortTermArtists():
    flash('These are your top artists. . .')
    flash('')
    l = findTopArtists()
    for artist in l:
        flash(artist)
    return render_template('shortTerm.html')

@app.route('/shortTermGenres')
def shortTermGenres():
    flash('These are your top music genres. . .')
    flash('')
    l = gatherGenres()
    for idx, genre in enumerate(l):
        flash(str(idx+1) + '. ' + str(genre))
    return render_template('shortTerm.html')

#medium term ###########################################
@app.route('/mediumTermSongs')
def mediumTermSongs():
    flash('These are your top songs. . .')
    flash('')
    l = findTopSongs()
    dev = findMood()
    for i in range(len(l)):
        flash(l[i]+ dev[i])
    flash('')
    flash('Your average song popularity is ' + str(round(findAvgSongPop(l), 2)))
    return render_template('mediumTerm.html')

@app.route('/mediumTermArtists')
def mediumTermArtists():
    flash('These are your top artists. . .')
    flash('')
    l = findTopArtists()
    for artist in l:
        flash(artist)
    return render_template('mediumTerm.html')

@app.route('/mediumTermGenres')
def mediumTermGenres():
    flash('These are your top music genres. . .')
    flash('')
    l = gatherGenres()
    for idx, genre in enumerate(l):
        flash(str(idx+1) + '. ' + str(genre))
    return render_template('mediumTerm.html')

#long term ##########################################
@app.route('/longTermSongs')
def longTermSongs():
    flash('These are your top songs. . .')
    flash('')
    l = findTopSongs()
    dev = findMood()
    for i in range(len(l)):
        flash(l[i]+ dev[i])
    flash('')
    flash('Your average song popularity is ' + str(round(findAvgSongPop(l), 2)))
    return render_template('longTerm.html')

@app.route('/longTermArtists')
def longTermArtists():
    flash('These are your top artists. . .')
    flash('')
    l = findTopArtists()
    for artist in l:
        flash(artist)
    return render_template('longTerm.html')

@app.route('/longTermGenres')
def longTermGenres():
    flash('These are your top music genres. . .')
    flash('')
    l = gatherGenres()
    for idx, genre in enumerate(l):
        flash(str(idx+1) + '. ' + str(genre))
    return render_template('longTerm.html')









@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')
    




# @app.route('/playlists')
# def playlists():
#     spotify = getToken()
#     return [i['name'] for i in spotify.current_user_playlists()['items']]


# @app.route('/currently_playing')
# def currently_playing():
#     spotify = getToken()
#     track = spotify.current_user_playing_track()
#     if not track is None:
#         return track['item']['name']
#     return "No track currently playing."


# @app.route('/current_user')
# def current_user():
#     spotify = getToken()
#     return spotify.current_user()

def getToken():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler, 
                                                client_id= SPOTIPY_CLIENT_ID,
                                                client_secret= SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


#finds top songs depending on the time range. returns thme in a list
def findTopSongs():
    print(TR)

    sp = getToken()
    results = sp.current_user_top_tracks(time_range=TR)
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


    sp = getToken()
    top_artists = sp.current_user_top_artists(time_range=TR)
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
    sp = getToken()
    results = sp.current_user_top_tracks(time_range=TR)
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
        dev.append((round(m['danceability']*100, 2), round(m['energy']*100, 2), round(m['valence']*100, 2)))
    
    
    return dev

def gatherGenres():
    spotify = getToken()
    top_artists = spotify.current_user_top_artists(time_range=TR)
    artists = top_artists['items']
    while top_artists['next']:
        top_artists = spotify.next(top_artists)
        artists.extend(top_artists['items'])
    
    d = {}
    for i in artists:
        for genre in i['genres']: #[hip hip, pop, rnb]
            if genre in d:
                d[genre] += 1
            else:
                d[genre] = 1
    return reversed([k for k, v in sorted(d.items(), key=lambda item: item[1])])

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

'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))

