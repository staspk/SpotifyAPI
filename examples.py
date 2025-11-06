import sys, subprocess
from kozubenko.env import Env
from kozubenko.print import Print
from spotify_py import auth_server
from spotify_py.SpotifyUser import SpotifyUser


"""
I want to see all my Liked Songs that are duplicates.
"""
NAME = "Stan"
subprocess.run([sys.executable, "import_spotify_data.py", NAME])

stan = SpotifyUser(NAME)
for duplicate in stan.songs_duplicates:
    Print.green(duplicate.console_report())


"""
stan_luna_compared.py moved here.
"""
Env.load()
auth_server.validate_token()
access_token = Env.vars['access_token']

Stan = SpotifyUser('Stan')
Luna = SpotifyUser('Luna')

shared = Luna.compareStreamedSongs(Stan)

for song1, song2 in shared:
    Print.cyan(f'{song1.title} - {song1.artist}. Luna: {song1.total_ms_played / 1000 / 60:.0f}mins. Stan: {song2.total_ms_played / 1000 / 60:.0f}mins.\n')

print(len(shared))