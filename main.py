import auth_server
from kozubenko.utils import *
from spotify_api.spotify_requests import *
from spotify_stats import SpotifyUser
from kozubenko.env import Env

from definitions import SPOTIFY_USER_DATA_DIR


if __name__ == '__main__':
    Env.load()
    auth_server.validate_token()
    access_token = Env.vars['access_token']

    Stan = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Stan')

    response = SaveToPlaylistRequest.New_Playlist(
        access_token,
        'staspk',
        'Playlist1'
    ).Handle(list[Song]).Result(True)