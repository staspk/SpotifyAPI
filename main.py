from spotify_py.spotify_requests import *
from spotify_py.SpotifyUser import SpotifyUser




ME = SpotifyUser('Stan')
HER = SpotifyUser('Luna')

her_favorite_songs = SpotifyUser.I_want_her_favorite_songs(ME, HER, minimum_listen_time_in_hours = 3)


exit(0)


response = SaveToPlaylistRequest.New_Playlist(
    access_token,
    'staspk',
    'Luna Low Grade',
    description='35mins < listen_time < 60mins'
).Handle(luna_list).Result(True)