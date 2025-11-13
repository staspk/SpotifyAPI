import http
import os
from time import sleep

import werkzeug
from kozubenko.os import File
from kozubenko.string import String
from spotify_py.spotify_auth import AuthServer
from kozubenko.print import Print
from spotify_py.spotify_requests import *
from spotify_py.SpotifyUser import SpotifyUser
from kozubenko.env import Env
from definitions import PROJECT_ROOT_DIRECTORY, SPOTIFY_USER_DATA_DIR



time.sleep(12)



Print.green('now here')

exit(0)


if __name__ == '__main__':
    ME = SpotifyUser('Stan')
    HER = SpotifyUser('Luna')

    her_favorite_songs = SpotifyUser.I_want_her_favorite_songs(ME, HER, minimum_listen_time_in_hours = 3)

    Env.load()
    auth_server2.validate_token()
    access_token = Env.vars['access_token']




    exit(0)


    response = SaveToPlaylistRequest.New_Playlist(
        access_token,
        'staspk',
        'Luna Low Grade',
        description='35mins < listen_time < 60mins'
    ).Handle(luna_list).Result(True)