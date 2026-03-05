"""
`SpotifyUser` deals with three types of user data:
    1. Spotify Account Data
    2. Spotify Extended Streaming History
    3. Spotify Technical Log Information

Request Data from Spotify: https://www.spotify.com/us/account/privacy/
    Data Details: https://support.spotify.com/us/article/understanding-your-data/
"""
from datetime import datetime
from Spotify_Data_Types import USER_DATA_DIR, Spotify_Data_Type
from kozubenko.os import Directory, File
from kozubenko.json import Json
from kozubenko.print import Print
from kozubenko.string import Str
from .spotify_requests import SimpleRequests
from .extended_streaming_history import AudioStreamingHistory, ExtendedStreamingHistory
from .account_data import AccountData, DuplicateSong
from .models.ISong import ISong
from .models.IStreamed import StreamedSong


def ACCOUNT_DATA(name:str):               return USER_DATA_DIR(name, Spotify_Data_Type.ACCOUNT_DATA)
def EXTENDED_STREAMING_HISTORY(name:str): return USER_DATA_DIR(name, Spotify_Data_Type.EXTENDED_STREAMING_HISTORY)

type occurrences = int

class SpotifyUser:
    """
    Use `py ./import_Spotify_Data.py {name}` to import `my_spotify_data.zip`. Data types Spotify offers:
    1. Spotify Account Data
    2. Spotify Extended Streaming History
    3. Spotify Technical Log Information

    ***Instantiate `SpotifyUser` with same `name` to manipulate/transform above data [1-2] to find statistical insights.***
    """
    @property
    def liked_songs(self) -> list[ISong]: return self._songs_liked

    def __init__(self, name:str):
        self.name = name

        self._account_creation_time:datetime = None
        if(data := Json.Exists(ACCOUNT_DATA(name), 'Userdata.json')):
            self._account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")

        self._songs_liked:set[ISong]; self._song_duplicates:list[DuplicateSong]
        if(data := Json.Exists(ACCOUNT_DATA(name), 'YourLibrary.json')):
            self._songs_liked, self._song_duplicates = AccountData.YourLibrary(data)

        self._history:AudioStreamingHistory = ExtendedStreamingHistory.Audio(
            name,
            EXTENDED_STREAMING_HISTORY(name).files(filter='Streaming_History_Audio')
        )

    def song_streaming_history(self, minimum_listen_time_in_minutes = 30) -> list[StreamedSong]:
        """ Required: `Spotify Extended Streaming History`  """
        return [song for song in self._history.songs if (song.total_ms_played > minimum_listen_time_in_minutes*60*1000)]
    
    def favorite_songs(self, minimum_listen_time_in_hours = 3) -> list[StreamedSong]:
        """ Required: `Spotify Extended Streaming History`  """
        return [song for song in self.song_streaming_history(minimum_listen_time_in_hours*60)]

    def lost_song_candidates(self, minimum_listen_time_in_minutes = 20) -> list[StreamedSong]:
        """
        technically: `self.song_streaming_history(minimum_listen_time_in_minutes=20)` NOT IN `self.liked_songs`

        **Required:**
            - `Spotify Extended Streaming History`
            - `Spotify Account Data`
        """
        return [song for song in self.song_streaming_history(minimum_listen_time_in_minutes) if song not in self._songs_liked]

    def Save_Liked_Songs(self) -> dict[ISong, occurrences]:
        """
        Uses Spotify WebApi instead. Saves as binary file in: `USER_DATA_DIR(name)`.

        Eventually, one could swap out:  
            - `SpotifyUser().liked_songs` WITH:
            - `SpotifyUser.Liked_Songs()
        when requirements for one or the other can't be met.

        **PARAMETERS:**
            - `name` - Same `name` you use to init: `SpotifyUser(name)`

        **REQUIRED:** `.env` key/value:
            - `client_id`
            - `client_secret`
        """
        liked_songs = SimpleRequests.Liked_Songs()

        file = File(USER_DATA_DIR(self.name), 'liked_songs').save_binary(liked_songs)
        Print.green(f'SpotifyUser.Save_Liked_Songs(): saved {len(liked_songs)} songs: {file}')
        
        return liked_songs


def Her_favorite_songs_minus_what_I_already_liked(Her:SpotifyUser, Me:SpotifyUser, minimum_listen_time_in_hours = 3) -> list[StreamedSong]:
    """
    **Returns**:
        `Her.song_streaming_history`, subtracted by `Me.songs_liked`, filtered by: `minimum_listen_time_in_hours`.

    **Required:**
        - `Spotify Extended Streaming History` FOR `Her`
        - `Spotify Account Data` FOR `Me`
    """
    return [song for song in Her.song_streaming_history(minimum_listen_time_in_hours*60) if song not in Me._songs_liked]

def have_I_lost_a_song_from_Liked(name:str) -> list[ISong]:
    """
    - `name` - Same `name` you use to init: `SpotifyUser(name)`

    Will check against your last backup. To do an actual backup, use: `SpotifyUser.Save_Liked_Songs()`
    """
    actual_Liked = SimpleRequests.Liked_Songs()
    backup_Liked:dict[ISong, occurrences] = File(USER_DATA_DIR(name), 'liked_songs').load_binary()

    missing:list[ISong] = []
    for song in backup_Liked.keys():
        if song not in actual_Liked.keys():
            missing.append(song)

    if len(missing) < 1:
        Print.green(f'No, {name}: you have NOT lost any songs :)') 
    else:
        Print.red(f'Yes, {name}: you have lost {len(missing)} songs...\n')
        for song in missing:
            Print.lite_red(Str(str(song)).pad(1))
        if len(missing) > 10:
            Print.red(f'\nYes, {name}: you have lost {len(missing)} songs...')

    return missing
