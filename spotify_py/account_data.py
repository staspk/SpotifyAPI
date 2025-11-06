from dataclasses import dataclass
from typing import Any
from .ISong import ISong


@dataclass()
class DuplicateSong():
    song: ISong
    total_duplicates: int = 1

    def console_report(self):
        return f'{str(self.song)} -> {self.total_duplicates}'


class ILikedSongs():
    """
    Requires: `/Spotify User Data/{name}/Spotify Account Data/YourLibrary.json`

    Note: `YourLibrary.json` does not preserve order by time added.
    """
    songs_liked:       set[ISong]
    songs_duplicates:  list[DuplicateSong]


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
        
        liked:       set[ISong]                   = set()
        duplicates:  dict[ISong, DuplicateSong]   = {}

        for record in data['tracks']:
            song = ISong(record['track'], record['artist'], record['album'])

            if(song in liked):
                duplicate = duplicates.pop(song, DuplicateSong(song))
                duplicate.total_duplicates += 1
                duplicates[duplicate.song] = duplicate
            else:
                liked.add(song)

        return (liked, duplicates.values())
