import spotify_py.auth_server as auth_server
from kozubenko.print import Print
from spotify_py.SpotifyUser import SpotifyUser
from spotify_py.spotify_requests import *

from kozubenko.env import Env

from definitions import SPOTIFY_USER_DATA_DIR


if __name__ == '__main__':
    Env.load()
    auth_server.validate_token()
    access_token = Env.vars['access_token']

    Stan = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Stan')
    Luna = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Luna')

    shared = Luna.compareStreamedSongs(Stan)

    for song1, song2 in shared:
        Print.cyan(f'{song1.title} - {song1.artist}. Luna: {song1.total_ms_played / 1000 / 60:.0f}mins. Stan: {song2.total_ms_played / 1000 / 60:.0f}mins.\n')

    print(len(shared))