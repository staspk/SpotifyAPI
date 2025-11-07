from kozubenko.os import File, Downloads_Directory
from kozubenko.print import Print
from kozubenko.string import String
from spotify_py.SpotifyUser import SpotifyUser



"""
I want my wife's true favorite songs (minus what I have already liked).
    Assumes: you have already imported the necessary Spotify Data Types.
        ie: `Spotify Account Data` for `me`, `Spotify Extended Streaming History` for `her`
"""
ME = SpotifyUser('Stan')
HER = SpotifyUser('Luna')

her_favorite_songs = SpotifyUser.I_want_her_favorite_songs(ME, HER, minimum_listen_time_in_hours = 3)

File(Downloads_Directory(), "her_favorite_songs.txt").save(String.list(her_favorite_songs, flip=True))
Print.green(f'Found {len(her_favorite_songs)} songs that {HER.name} truly loved')
Print.yellow(f'her_favorite_songs.txt can be found in your Downloads folder :)')
