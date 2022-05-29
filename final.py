import spotipy
import spotipy.util as util
import time
from RPi import GPIO
from RPLCD.gpio import CharLCD
import secrets

class SpotifyCurrentTrack:

    def __init__(self, username, spotify_client_id, spotify_secret, scope):
        self.username = username
        self.spotify_client_id = spotify_client_id
        self.spotify_secret = spotify_secret
        self.scope = scope

    def GetToken(self):
        token =  util.prompt_for_user_token(username,
                                            scope=scope,
                                            client_id=spotify_client_id,
                                            client_secret=spotify_secret,
                                            redirect_uri='https://accounts.spotify.com/authorize')
        return token

    def GetCurrentSong(self, token):
        sp = spotipy.Spotify(auth=token)
        track = sp.current_playback(market='PL')
        artist_temp = track['item']['artists']
        artist = ''
        for artists in artist_temp:
            artist = artist + artists['name'] + ', '
    
        artist = artist[:-2]
        song_name = track['item']['name']
        return artist, song_name

def write_to_lcd(lcd, framebuffer, num_cols):
    """Write the framebuffer out to the specified LCD."""
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')

def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.4):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)

username = secrets.username
scope = secrets.scope
spotify_client_id = secrets.spotify_client_id
spotify_secret = secrets.spotify_secret
lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD)
framebuffer = [
    '',
    '',
]


client = SpotifyCurrentTrack(username, spotify_client_id, spotify_secret, scope)
token =  client.GetToken()
if client.GetCurrentSong(token):
    current_artist, current_song_name = client.GetCurrentSong(token)
    if len(current_artist) > 16:
        loop_string(current_artist, lcd, framebuffer, 0, 16)
        loop_string(current_song_name, lcd, framebuffer, 1, 16)
    else:
        lcd.home()
        lcd.write_string(current_artist)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(current_song_name)
    

try:
    while True:
        artist, song_name = client.GetCurrentSong(token)
        if artist != current_artist and song_name != current_song_name:
            current_artist, current_song_name = artist, song_name
            
        time.sleep(5)
finally:
    lcd.close(clear=True)
    GPIO.cleanup()