"""
Spotify Extended Streaming History
    "master_metadata_album_artist_name" -> tracks only one artist, evidently: artists[0] from: https://api.spotify.com/v1/tracks/{id}
"""
from dataclasses import dataclass


@dataclass
class ISong:
    """
    **Attributes:**
        - `artist` - e.g: `San Holo`
            - Extended Streaming History, tracks only one artist, evidently `artists[0]` from: https://api.spotify.com/v1/tracks/{id}
            e.g: `"master_metadata_album_artist_name": "San Holo"`
    """
    title: str
    artist: str
    album: str

    def __eq__(self, other):
        if not isinstance(self, ISong):
            return False
        return (self.title == other.title and self.artist == self.artist and self.album == other.album)
    
    def __hash__(self):
        return hash((self.title, self.artist, self.album))
    
    def __str__(self):
        return f'{self.title}:{self.artist}'