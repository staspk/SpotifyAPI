import os
import time
import auth_server
from spotify_requests import SpotifyRequests
from spotify_stats import SpotifyUser
from kozubenko.env import Env
from kozubenko.timer import Timer

from definitions import PROJECT_ROOT_DIRECTORY

for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT_DIRECTORY):
    print(f"dirpath: {dirpath}")
    print(f"dirnames: {dirnames}")
    print(f"filenames: {filenames}")
    print('\n')



# song_list = SpotifyUser(r'Spotify_Data\Stan.zip').getSortedSongStreamingHistory(30)


# for song in song_list:
#     print(str(song))


# if auth_server.hasAuthTokenExpired(True):
#     auth_server.start_local_http_server()

    


#     auth_server.stop_local_http_server()

#     print('reached')
    

    # time.sleep(120)

    # SpotifyRequests.saveStreamingHistoryToSpotifyPlaylist(song_list,
    #                                               playlist_name=f"What She Actually Loved",
    #                                               description=f'I will find the average song length * 7 listens sometime soon and that will be the cutoff')


# Timer.stop()







