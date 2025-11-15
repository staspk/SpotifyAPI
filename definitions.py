import os


#----- Spotify Web API / Spotify Authorization Code Flow ---------------------------------#
REDIRECT_URI      = 'http://127.0.0.1:8080/callback'
PERMISSION_SCOPES = 'playlist-read-private playlist-read-collaborative user-library-read user-library-modify playlist-modify-public user-top-read'


#----- Spotify Data Types (aka: the folder inside 'my_spotify_data.zip') -----------------#
SPOTIFY_ACCOUNT_DATA                =  'Spotify Account Data'
SPOTIFY_EXTENDED_STREAMING_HISTORY  =  'Spotify Extended Streaming History'
SPOTIFY_TECHNICAL_LOG               =  'Spotify Technical Log Information'



#----- Absolute Paths to Project Directories ---------------------------------------------#
PROJECT_ROOT_DIRECTORY          =  os.path.dirname(os.path.abspath(__file__))
ENV                             =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env')
SPOTIFY_USER_DATA_DIR           =  os.path.join(PROJECT_ROOT_DIRECTORY, 'Spotify User Data')
SPOTIFY_USER_DATA_ARCHIVE_DIR   =  os.path.join(SPOTIFY_USER_DATA_DIR,  'Spotify User Data', 'Archive')



APP_NAME = 'SpotifyApi'