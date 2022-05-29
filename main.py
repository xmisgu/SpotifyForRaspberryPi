import spotipy
from time import sleep
import spotipy.util as util
import secrets

spotify_client_id = secrets.spotify_client_id
spotify_secret = secrets.spotify_secret
username = secrets.username
scope = secrets.scope
token =  util.prompt_for_user_token(username,
                           scope=scope,
                           client_id=spotify_client_id,
                           client_secret=spotify_secret,
                           redirect_uri='https://accounts.spotify.com/authorize')


sp = spotipy.Spotify(auth=token)

track = sp.current_playback(market='PL')
artist_temp = track['item']['artists']

song = ''
for artist in artist_temp:
    song = song + artist['name'] + ', '
    
song = song[:-2]

song = song +  ' - ' + track['item']['name']
current_song = song
print(song)

while True:
    track = sp.current_playback(market='PL')
    artist_temp = track['item']['artists']

    song = ''
    for artist in artist_temp:
        song = song + artist['name'] + ', '
    
    song = song[:-2]

    song = song +  ' - ' + track['item']['name']

    if(song != current_song):
        current_song = song
        print(current_song)



