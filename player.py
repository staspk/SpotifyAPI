"""
    A server, that checks what song is playing in a loop.
    For ruined songs that have golden parts, but the rest is whiny / sinful / bitchy (of such a low quality, that it would be harmful to hear)
"""

import json
from kozubenko.io import load_json
from spotify_models import ISong


songs:list[ISong] = load_json("restricted_songs.json", ISong)

print(json.dumps(songs, indent=4))

while True:
    break