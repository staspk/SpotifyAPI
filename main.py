from spotify import Spotify
from kozubenko.env import Env

Stan = Spotify(r'Spotify_Data\Stan').getSortedSongStreamingHistory(1800)
Luna = Spotify(r'Spotify_Data\Luna').getSortedSongStreamingHistory(1800)




