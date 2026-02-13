from kozubenko.os import Downloads_Directory, File
from kozubenko.print import Print
from kozubenko.string import Str
from spotify_py.spotify_requests import SimpleRequests, SaveToPlaylistRequest
from spotify_py.SpotifyUser import SpotifyUser, I_want_her_favorite_songs
from import_Spotify_Data import Import_Spotify_Data



"""
"I want my Wife's true favorite songs, based on Her entire Spotify listening history, minus my Liked Songs"
    Assumes: you have already imported the necessary Spotify Data Types; ie:
        - `Spotify Account Data` for `ME`,                via: `py ./import_spotify_data.py Stan`
        - `Spotify Extended Streaming History` for `HER`, via: `py ./import_spotify_data.py Luna`
"""
ME = SpotifyUser('Stan')
HER = SpotifyUser('Luna')

her_favorite_songs = I_want_her_favorite_songs(ME, HER, minimum_listen_time_in_hours = 1)
File(Downloads_Directory(), "her_favorite_songs.txt").save(Str.From(her_favorite_songs))


"""
"I want a Spotify playlist created from Her favorite 1000 songs" 
    Assumes: you've created an app on: https://developer.spotify.com/dashboard,
             client_id, client_secret set in file ./.env
"""
SaveToPlaylistRequest.New_Playlist(
    playlist_name='Her Favorite Songs',
    description='upper segment of her lifetime_listening_record (1hr) - songs_I_already_liked'
).Handle(her_favorite_songs).Result()
