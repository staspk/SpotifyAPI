from collections import namedtuple
from dataclasses import dataclass
import os, json
from datetime import datetime
from typing import Self
from kozubenko.print import *
from kozubenko.os import Directory, File
from kozubenko.utils import Json
# from spotify_py.ISong import ISong
from spotify_py.ISong import ISong
from spotify_py.IStreamed import IStreamed, AudioBook, StreamedSong, Podcast
from spotify_py.extended_streaming_history import AudioStreamingHistory
from definitions import SPOTIFY_USER_DATA_DIR


@dataclass()
class LikedSong(ISong):
    uri:str

    def __repr__(self):
        return f'LikedSong:{self.title}:{self.artist}'
    


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
        self.account_creation_time:datetime

        self.songs_liked:       dict[str, LikedSong]
        self.songs_duplicates:  dict[str, int]

        history: AudioStreamingHistory = None

        # if(ACCOUNT_DATA := Directory.exists(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Account Data')):
        #     if(file := File.exists(ACCOUNT_DATA, 'Userdata.json')):
        #         with open(file, 'r') as _json:
        #             data = json.load(_json)
        #             self.account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")

        #     if(_json := File.exists(ACCOUNT_DATA, 'YourLibrary.json')):
        #         (self.songs_liked, 
        #          self.songs_duplicates) = SpotifyUser.parseLikedSongs(_json)

        if(dir := Directory.exists(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Extended Streaming History')):
            if(files := Directory.files(dir, 'Streaming_History_Audio')):
                self.history = AudioStreamingHistory.From(files)
                self.history.console_report()

                songs = self.history.songs
                # print_yellow(type(self.history.songs_streamed))

        
    

    @staticmethod
    def parseLikedSongs(json:str):
        songs_liked:       dict[str, LikedSong]
        songs_duplicates:  dict[str, int]

        for record in Json.from_file(json)['tracks']:
            song = LikedSong(record['track'], record['artist'], record['album'], record['uri'])

            fromLiked = songs_liked.get(repr(song), None)
            if fromLiked is None:
                songs_liked[repr(song)] = song
            else:
                numOfDuplicates = songs_duplicates.pop(repr(song), 0)
                songs_duplicates[repr(song)] = (numOfDuplicates + 1)

        return (songs_liked, songs_duplicates)


    def _getSortedList(dictInQuestion, minsCutoff) -> list:
        toReturnList = []
        msCutoff = (minsCutoff * 60 * 1000)

        for song in dictInQuestion.values():
            if song.total_ms_played > msCutoff:
                toReturnList.append(song)

        toReturnList.sort()
        # print(f'Sorting done in _getSortedList(). toReturnList Count: {len(toReturnList)}')
        return toReturnList

    def getSortedSongStreamingHistory(self, minsCutoff = 30, ascending=False) -> list[StreamedSong]:
        list = SpotifyUser._getSortedList(self.songs_streamed, minsCutoff)
        if not ascending:
            list.sort(key=lambda song: song.total_ms_played, reverse=True)
        return list
    
    def getSortedPodcastStreamingHistory(self, minsCutoff = 30) -> list[StreamedSong]:
        return SpotifyUser._getSortedList(self.podcasts_streamed, minsCutoff)
    
    def printDuplicateSongs(self):
        for key, value in self.songs_duplicates.items():
            print(f'{key}: {value}')
        print(f'Total: {len(self.songs_duplicates)}')

    def printLikedSongs(self):
        for song in SpotifyUser.songs_liked:
            print(str(song))
            print()
        print(f'Total: {len(SpotifyUser.songs_liked)}')

    def getLikedSongs(self) -> list:
        liked_songs_list = list(self.songs_liked.values())

        # liked_songs_list = [ISong(value) for value in self.songs_liked.values()]

        return liked_songs_list

    def compareStreamedSongs(self, other:Self, min_mins_cutoff = 20) -> list[tuple[StreamedSong, StreamedSong]]:
        if not isinstance(other, SpotifyUser):
            return AssertionError('other must be an instance of SpotifyUser')
        
        MS_CUTOFF = (min_mins_cutoff * 60 * 1000)
        
        my_list = [song for song in self.songs_streamed.values() if song.total_ms_played > MS_CUTOFF]
        other_list = [song for song in other.songs_streamed.values() if song.total_ms_played > MS_CUTOFF]


        
        list1 = self.getSortedSongStreamingHistory(min_mins_cutoff)
        list2 = other.getSortedSongStreamingHistory(min_mins_cutoff)
        shared_songs: list[tuple[StreamedSong, StreamedSong]] = []
        
        for song1 in list1:
            for i in range(len(list2)):
                if song1 == list2[i]:
                    shared_songs.append((song1, list2[i]))

        return shared_songs

    def getLostSongCandidates(self, min_mins_listened=20) -> list[StreamedSong]:
        """
        Required:\n
        - Spotify Account Data
        - Extended Streaming History

        Will get a list of your most listened songs that exceed min_mins_listened, subtract your Liked Songs from it, and return That
        """
        if len(self.songs_streamed) == 0:
            raise AssertionError('Can only call SpotifyUser.getLostSongCandidates() if Spotify has been fed the "Spotify Extended Streaming History" json data.')
        
        msCutoff = (min_mins_listened * 60 * 1000)
        songsStreamedCopy = {}

        for song in self.songs_streamed.values():
            if song.total_ms_played > msCutoff:
                songsStreamedCopy[repr(song)] = song

        if len(self.songs_liked) > 0:
            for song in self.songs_liked.values():
                songsStreamedCopy.pop(repr(song), None)

        count = 0
        for song in songsStreamedCopy.values():
            count +=1

        candidateList = list(songsStreamedCopy.values())
        candidateList.sort()
        return candidateList

    def saveLostSongCandidatesToFile(self, minsCutoff=10, toFile=r'.\lost_song_candidates.txt'):
        candidates = self.getLostSongCandidates(minsCutoff)
        SpotifyUser.saveListToFile(candidates, toFile)
        print(f'Lost Song Candidate file created at: {os.path.abspath(toFile)}')

    def saveListToFile(list, file_path=r'.\out.txt'):
        with open(fr'{file_path}', 'w', ) as file:
            for item in list:
                file.write(str(item))
                file.write('\n\n')

