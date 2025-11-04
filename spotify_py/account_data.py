from dataclasses import dataclass
from typing import Any
from .ISong import ISong


@dataclass()
class LikedSong(ISong):
    """
    An instance from `YourLibrary.json['tracks']`  

    `uri` - example form: `spotify:track:4Bxl1qty34HSOKZrRjyj0s`  
    """
    uri:str

    def __repr__(self):
        return f'LikedSong:{self.title}:{self.artist}'


class ILikedSongs():
    """
    Requires: `/Spotify User Data/{name}/Spotify Account Data/YourLibrary.json`

    Note: `YourLibrary.json` does not preserve order by time added.
    """
    songs_liked:       list[LikedSong]
    songs_duplicates:  dict[LikedSong, int]     # duplicates are found on basis of [song title + artist name] under the hood. See: `ISong`


class AccountData:
    """
    **Requires:** `/Spotify User Data/{name}/Spotify Account Data`.  
    
    ***See: `SpotifyUser.py` for import steps.***
    """
    def Parse(name:str, data:Any) -> ILikedSongs:
        """
        **Theoretical Breakage Point:**
            - 1,171 liked songs generated ~7067 lined `YourLibrary.json`
            - 387,000 lines lowest limit for `Streaming_History_Audio_***.json`
            - `AccountData.LikedSongs()` theoretical upper limit: `SpotifyUser.liked.count > 63,234`
        """
        
        songs_liked:       dict[str, LikedSong] = {}
        songs_duplicates:  dict[str, int]       = {}

        for record in data['tracks']:
            song = LikedSong(record['track'], record['artist'], record['album'], record['uri'])

            fromLiked = songs_liked.get(repr(song), None)
            if fromLiked is None:
                songs_liked[repr(song)] = song
            else:
                numOfDuplicates = songs_duplicates.pop(repr(song), 0)
                songs_duplicates[repr(song)] = (numOfDuplicates + 1)

        return (
            songs_liked.values(), songs_duplicates
        )