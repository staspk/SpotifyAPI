import os


APP_NAME = 'SpotifyApi'

#----- Spotify Web API / Spotify Authorization Code Flow ---------------------------------#
REDIRECT_URI      = 'http://127.0.0.1:8080/callback'
PERMISSION_SCOPES = 'playlist-read-private playlist-read-collaborative user-library-read user-library-modify playlist-modify-public user-top-read'


#----- Absolute Paths to Project Directories / Config Files ---------------------------------------------#
PROJECT_ROOT_DIRECTORY =  os.path.dirname(os.path.abspath(__file__))
SPOTIFY_USER_DATA_DIR  =  os.path.join(PROJECT_ROOT_DIRECTORY, 'Spotify User Data')
ENV                    =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env')


#----- Spotify User Data :: Data Owners ---------------------------------------------#
STAN = os.path.join(PROJECT_ROOT_DIRECTORY, 'Spotify User Data', 'Stan')
LUNA = os.path.join(PROJECT_ROOT_DIRECTORY, 'Spotify User Data', 'Luna')


TEMP_DIR = os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')
