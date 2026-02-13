from dataclasses import dataclass
from typing import Any
from .models.ISong import ISong


@dataclass
class DuplicateSong:
    song: ISong
    total_duplicates: int = 1

    def console_report(self):
        return f'{str(self.song)} -> {self.total_duplicates}'


type songs_liked = set[ISong]
type song_duplicates = list[DuplicateSong]

class AccountData:
    """
    **Requires:** `/Spotify User Data/{name}/Spotify Account Data`.  
    
    ***See: `SpotifyUser.py` for import steps.***
    """

    @staticmethod
    def YourLibrary(data:Any) -> tuple[songs_liked, song_duplicates]:
        """
        **Requires:** `/Spotify User Data/{name}/Spotify Account Data/YourLibrary.json`  
            - `data` - pass in above file with: `json.load(file)`

        Note: `YourLibrary.json` does not preserve order by time added! If required, use WebApi:
            - https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks

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
