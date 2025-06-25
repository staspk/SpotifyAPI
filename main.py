import os
import spotify_py.auth_server as auth_server
from kozubenko.print import *
from spotify_py.spotify_requests import *
from spotify_py.spotify_stats import SpotifyUser
from kozubenko.env import Env




NAME = 'Stan'

lost_song_candidates = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}{os.path.sep}{NAME}').getLostSongCandidates(min_mins_listened=60)



exit(0)


lost_song_candidates = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}{os.path.sep}{NAME}').getLostSongCandidates(min_mins_listened=60)

SaveToPlaylistRequest.New_Playlist(
	access_token,
	user_name,
	playlist_name,
	description
).Handle(lost_song_candidates).Result(True)

exit(0)

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