from multiprocessing import Process
import multiprocessing
import os
import subprocess
import sys
import threading
import time
import auth_server
from kozubenko.utils import *
from spotify_requests import SpotifyRequests
from spotify_stats import SpotifyUser
from kozubenko.env import Env
from kozubenko.timer import Timer

from definitions import SPOTIFY_USER_DATA_DIR




if __name__ == '__main__':
    auth_server.validate_token()

    SpotifyRequests.get_user_id(None)


    
    
    
    

# SpotifyRequests.saveStreamingHistoryToSpotifyPlaylist(
#     song_list,
#     playlist_name=f"What She Actually Loved",
#     description=f'I will find the average song length * 7 listens sometime soon and that will be the cutoff'
# )


# Timer.stop()

# if __name__ == '__main__':
#     auth_server.validate_token(True)







