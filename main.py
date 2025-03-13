from multiprocessing import Process
import multiprocessing
import os
import subprocess
import sys
import threading
import time
import auth_server
from kozubenko.utils import *
from spotify_api.spotify_requests import SimpleRequests
from spotify_stats import SpotifyUser
from kozubenko.env import Env
from kozubenko.timer import Timer

from definitions import SPOTIFY_USER_DATA_DIR




if __name__ == '__main__':
    Env.load()
    auth_server.validate_token()
    access_token = Env.vars['access_token']


    # SpotifyRequests.create_spotify_playlist('staspk')

    # handledReq = CreatePlaylistRequest('stasp', Env.vars['access_token']).Handle()

    # SaveToPlaylistRequest.Exising_Playlist(PlaylistId('4R79CbpxOWa95IGcm0Wtqu'))

    # SaveToPlaylistRequest('PlaylistName')

    # SimpleRequests.get_playlist('fghj', access_token)



    
    
    
    

# SpotifyRequests.saveStreamingHistoryToSpotifyPlaylist(
#     song_list,
#     playlist_name=f"What She Actually Loved",
#     description=f'I will find the average song length * 7 listens sometime soon and that will be the cutoff'
# )


# Timer.stop()

# if __name__ == '__main__':
#     auth_server.validate_token(True)







