from datetime import datetime
from kozubenko.os import Directory
from kozubenko.json import Json
from .account_data import AccountData, DuplicateSong
from .ISong import ISong
from .IStreamed import StreamedSong
from spotify_py.extended_streaming_history import AudioStreamingHistory, ExtendedStreamingHistory
from definitions import SPOTIFY_USER_DATA_DIR



class SpotifyUser:
    """
    Use `py ./import_spotify_data.py {name}` to import `my_spotify_data.zip`. Data types Spotify offers:
    1. Spotify Account Data
    2. Spotify Extended Streaming History
    3. Spotify Technical Log Information

    ***Instantiate `SpotifyUser` with same `name` to manipulate/transform above data [1-2] to find statistical insights.***
    """
    def __init__(self, name:str):
        self.name = name

        self._account_creation_time:datetime = None
        if(data := Json.exists(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Account Data', 'Userdata.json')):
            self._account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")

        self._songs_liked:list[ISong]; self._songs_duplicates:list[DuplicateSong]
        if(data := Json.exists(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Account Data', 'YourLibrary.json')):
            (self._songs_liked,
             self._songs_duplicates) = AccountData.Parse(self.name, data)

        self._history:AudioStreamingHistory = ExtendedStreamingHistory.Parse(
            self.name,
            Directory.files(
                Directory(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Extended Streaming History'),
                'Streaming_History_Audio'
            )
        )

    @staticmethod
    def I_want_her_favorite_songs(me:SpotifyUser, her:SpotifyUser, minimum_listen_time_in_hours = 3) -> list[StreamedSong]:
        """  technically: her `lifetime_listening_record`, filtered by `minimum_listen_time_in_hours`, subtracted by my `songs_liked`  
          
        **Requirements:**
            - `Spotify Account Data` for `me`
            - `Spotify Extended Streaming History` for `her` 
        """
        return [song for song in her.song_streaming_history(minimum_listen_time_in_hours*60) if song not in me._songs_liked]

    def favorite_songs(self, minimum_listen_time_in_hours = 3) -> list[StreamedSong]:
        """  technically: `lifetime_listening_record`, filtered by `minimum_listen_time_in_hours`
        Required: `Spotify Extended Streaming History`  """
        return [song for song in self.song_streaming_history(minimum_listen_time_in_hours*60)]

    def lost_song_candidates(self, minimum_listen_time_in_minutes = 20) -> list[StreamedSong]:
        """  technically: a minimum_listen_time_in_minutes-filtered `lifetime_listening_record` - `LikedSongs`  
        Required: `Spotify Extended Streaming History` + `Spotify Account Data`
        """
        return [song for song in self.song_streaming_history(minimum_listen_time_in_minutes) if song not in self._songs_liked]
    
    def song_streaming_history(self, minimum_listen_time_in_minutes = 30) -> list[StreamedSong]:
        """  technically: `lifetime_listening_record`, filtered by `minimum_listen_time_in_minutes`  
        Required: `Spotify Extended Streaming History`  """
        return [song for song in self._history.songs if (song.total_ms_played > minimum_listen_time_in_minutes*60*1000)]
