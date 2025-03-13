from multiprocessing import Process
import multiprocessing
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import auth_server
from kozubenko.utils import *
from spotify_api.spotify_requests import *
from spotify_stats import SpotifyUser
from kozubenko.env import Env
from kozubenko.timer import Timer

from definitions import SPOTIFY_USER_DATA_DIR




if __name__ == '__main__':
    Env.load()
    auth_server.validate_token()
    access_token = Env.vars['access_token']

    luna_songs = SpotifyUser(fr'{SPOTIFY_USER_DATA_DIR}\Luna').getSortedSongStreamingHistory(300)
    print(len(luna_songs))

    # SimpleRequests.get_playlist('7LmSTLoNwrzgTmBbMML9EV', access_token)
    # SimpleRequests.get_user_playlists(access_token)



    SaveToPlaylistRequest.New_Playlist('staspk', access_token, "Luna's Favorites").Handle(luna_songs).Result(True)
    # SaveToPlaylistRequest.Existing_Playlist(PlaylistId('7LmSTLoNwrzgTmBbMML9EV'), access_token).Handle(luna_songs).Result()




    
    
    
    

# SpotifyRequests.saveStreamingHistoryToSpotifyPlaylist(
#     song_list,
#     playlist_name=f"What She Actually Loved",
#     description=f'I will find the average song length * 7 listens sometime soon and that will be the cutoff'
# )


# Timer.stop()

# if __name__ == '__main__':
#     auth_server.validate_token(True)







