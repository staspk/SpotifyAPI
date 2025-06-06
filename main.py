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
    Luna = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Luna')

    

    luna = Luna.getSortedSongStreamingHistory(35)
    luna2 = Luna.getSortedSongStreamingHistory(60)
    stan = Stan.getLikedSongs()

    luna_minus_stan = [song for song in luna if song not in stan]
    luna_list       = [song for song in luna if song not in luna2]
    

    print_list(luna_list)
    print_red(luna_minus_stan.__len__())
    print_red(luna_list.__len__())

    # songs = Stan.compareStreamedSongs(Luna)
    # for stan_song, luna_song in songs:
    #     print_red(stan_song)
    #     print_red(luna_song)
    #     print()


    response = SaveToPlaylistRequest.New_Playlist(
        access_token,
        'staspk',
        'Luna Low Grade',
        description='35mins < listen_time < 60mins'
    ).Handle(luna_list).Result(True)