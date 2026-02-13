from dataclasses import dataclass
from spotify_py.models.ISong import ISong


@dataclass
class Track(ISong):
    """
    https://api.spotify.com/v1/tracks/{id}

    **Attributes:**
        - `id` - e.g: `7snnEDYwv30hRtmifVni8P`
            - Extended Streaming History, instead uses: `"spotify_track_uri": "spotify:track:7snnEDYwv30hRtmifVni8P"`
        - `added_at` - UTC timestamp, format: ISO-8601, e.g: `2026-02-11T07:57:54Z`
    """
    id:str
    added_at:str
