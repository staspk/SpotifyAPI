import os
import subprocess
import sys
import threading
import time
import auth_server
from spotify_requests import SpotifyRequests
from spotify_stats import SpotifyUser
from kozubenko.env import Env
from kozubenko.timer import Timer

from definitions import SPOTIFY_USER_DATA_DIR




# luna_list = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Luna').getSortedSongStreamingHistory(30)

print(SPOTIFY_USER_DATA_DIR)

stan_liked = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Stan').getLikedSongs()


for song in stan_liked:
    print(str(song))
    print()
print(len(stan_liked))

auth_server.validate_token()

# SpotifyRequests.saveStreamingHistoryToSpotifyPlaylist(song_list,
#                                               playlist_name=f"What She Actually Loved",
#                                               description=f'I will find the average song length * 7 listens sometime soon and that will be the cutoff')


# Timer.stop()







