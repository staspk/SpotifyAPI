from sys import getsizeof
from requests import request
import requests
from spotify_stats import SpotifyUser
from kozubenko.env import Env

SpotifyUser(r'Spotify_Data\Luna')
# print(f'Final Song Count: {len(Luna)}')
    

# print()

# Stan = Spotify(r'Spotify_Data\Stan').getSortedSongStreamingHistory(30)
# print(f'THE LENGTH: {len(Stan)}')



# Spotify.saveListToFile(Stan, toFile=r'.\generated_data\Stan_Top_Streamed.txt')
# Spotify.saveListToFile(Luna, toFile=r'.\generated_data\Luna_Top_Streamed.txt')

# _dict = Stan.songDuplicates
# print(type(_dict))

# for key, value in Stan.songDuplicates.items():
#     print(key)
#     print(value)
#     print()

