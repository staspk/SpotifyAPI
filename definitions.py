import os, time


#--- Absolute Paths to Project Directories ---------------------------------------------#
PROJECT_ROOT_DIRECTORY          =  os.path.dirname(os.path.abspath(__file__))
ENV                             =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env', '.env')
TEMP_DIR                        =  os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')
SPOTIFY_USER_DATA_DIR           =  os.path.join(PROJECT_ROOT_DIRECTORY, 'Spotify User Data')
SPOTIFY_USER_DATA_ARCHIVE_DIR  =  os.path.join(SPOTIFY_USER_DATA_DIR, 'Archive')

#--- 'my_spotify_data*.zip' Folder Names -----------------------------------------------#
SPOTIFY_ACCOUNT_DATA                =  'Spotify Account Data'
SPOTIFY_EXTENDED_STREAMING_HISTORY  =  'Spotify Extended Streaming History'
SPOTIFY_TECHNICAL_LOG               =  'Spotify Technical Log Information'


OS_TIMEZONE = time.tzname