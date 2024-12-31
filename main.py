from requests import request
from spotify import Spotify
from kozubenko.env import Env

# Luna = Spotify(r'Spotify_Data\Luna').getSortedSongStreamingHistory(1800)
# print(f'THE LENGTH: {len(Luna)}')

# print()

Stan = Spotify(r'Spotify_Data\Stan').getSortedSongStreamingHistory(1800)
# print(f'THE LENGTH: {len(Stan)}')



# Spotify.saveListToFile(Stan, toFile=r'.\generated_data\Stan_Top_Streamed.txt')
# Spotify.saveListToFile(Luna, toFile=r'.\generated_data\Luna_Top_Streamed.txt')

# _dict = Stan.songDuplicates
# print(type(_dict))

# for key, value in Stan.songDuplicates.items():
#     print(key)
#     print(value)
#     print()


