import os
import subprocess
import time
import auth_server
from spotify_requests import SpotifyRequests
from spotify_stats import SpotifyUser
from kozubenko.env import Env
from kozubenko.timer import Timer

from definitions import SPOTIFY_USER_DATA_DIR




song_list = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Stan').getSortedSongStreamingHistory(30)


for song in song_list:
    print(str(song))
    print()


# if not auth_server.validate_token(True):
#     auth_server.start_local_http_server()

#     time.sleep(3)

#     print('ive woken up')

#     auth_server.stop_local_http_server()

#     print('ive reached the end')
    

    # time.sleep(120)

    # SpotifyRequests.saveStreamingHistoryToSpotifyPlaylist(song_list,
    #                                               playlist_name=f"What She Actually Loved",
    #                                               description=f'I will find the average song length * 7 listens sometime soon and that will be the cutoff')


# Timer.stop()







