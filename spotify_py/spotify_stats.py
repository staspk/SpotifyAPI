import os, json
from datetime import datetime
from typing import Self
from kozubenko.print import print_green
from spotify_py.spotify_models import IStreamed, Song, LikedSong, Podcast
from definitions import SPOTIFY_USER_DATA_DIR


class SpotifyUser:
    """
    Use `py ./import_spotify_data.py {name}` to import `*.zip` Spotify Data, categorized by `name` of data owner. Data types Spotify offers:
    - Spotify Account Data
    - Spotify Extended Streaming History
    - Spotify Technical Log Information

    ***Instantiate `SpotifyUser` with same `name` to manipulate/transform above data to find statistical insights.***
    """
    def __init__(self, name:str):
        self.user_name = os.path.basename(spotify_data_dir)
        
        self.streaming_history_files:list = []
        self.your_library_json_file = None                          # Spotify Account Data/YourLibrary.json -> list of liked songs
        self.account_creation_time:datetime = None

        self.songs_streamed:    dict[str, Song]    = {}
        self.podcasts_streamed: dict[str, Podcast] = {}

        self.songs_liked:       dict[str, LikedSong] = {}
        self.songs_duplicates:  dict[str, int] = {}

        for file in os.listdir(spotify_data_dir):
            if file == 'Spotify Extended Streaming History':
                extended_streaming_history_dir = os.path.join(spotify_data_dir, file)
                for file_name in os.listdir(extended_streaming_history_dir):
                    if 'Streaming_History_Audio' in file_name:
                        self.streaming_history_files.append(os.path.join(extended_streaming_history_dir, file_name))

            if file == 'Spotify Account Data':
                spotify_account_data_dir = os.path.join(spotify_data_dir, file)
                for file_name in os.listdir(spotify_account_data_dir):
                    if file_name == 'YourLibrary.json':
                        self.your_library_json_file = os.path.join(spotify_account_data_dir, file_name)
                    if file_name == 'Userdata.json':
                        userData = os.path.join(spotify_account_data_dir, file_name)
                        with open(userData, 'r') as json_file:
                            data = json.load(json_file)
                            self.account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")

        if self.streaming_history_files:
            self._parseStreamingHistory()
        if self.your_library_json_file:
            self._parseLikedSongs()

    def _parseStreamingHistory(self):
        recordsIterated = 0
        for file in self.streaming_history_files:
            with open(file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for record in data:
                    audio:IStreamed = None
                    audio = IStreamed.createFromJsonRecord(record)

                    if isinstance(audio, Song):
                        representation = repr(audio)

                        fromDict = self.songs_streamed.pop(representation, None)
                        if fromDict is not None:
                            audio.combine(fromDict)
                        self.songs_streamed[representation] = audio

                    elif isinstance(audio, Podcast):
                        fromDict = self.podcasts_streamed.pop(repr(audio), None)
                        if fromDict is not None:
                            audio = audio.combine(fromDict)
                        self.podcasts_streamed[repr(audio)] = audio

                    elif audio is None:
                        # print(f"Garbage Data at Record Read Cycle: {recordsIterated}")
                        pass

                    else:
                        print(f"RuntimeError Reached on Cycle: {recordsIterated}")
                        raise RuntimeError('Neither Song nor Podcast')
                    
                    recordsIterated += 1
        print_green(f'{self.user_name}: iterated through {recordsIterated} records in Extended Streaming History')

    def _parseLikedSongs(self):
        with open(self.your_library_json_file, 'r', encoding='utf8') as file:
            data = json.load(file)
            for record in data['tracks']:
                song = LikedSong(record['track'], record['artist'], record['album'], record['uri'])

                fromLiked = self.songs_liked.get(repr(song), None)
                if fromLiked is None:
                    self.songs_liked[repr(song)] = song
                else:
                    numOfDuplicates = self.songs_duplicates.pop(repr(song), 0)
                    self.songs_duplicates[repr(song)] = (numOfDuplicates + 1)

    def _getSortedList(dictInQuestion, minsCutoff) -> list:
        toReturnList = []
        msCutoff = (minsCutoff * 60 * 1000)

        for song in dictInQuestion.values():
            if song.total_ms_played > msCutoff:
                toReturnList.append(song)

        toReturnList.sort()
        # print(f'Sorting done in _getSortedList(). toReturnList Count: {len(toReturnList)}')
        return toReturnList

    def getSortedSongStreamingHistory(self, minsCutoff = 30, ascending=False) -> list[Song]:
        list = SpotifyUser._getSortedList(self.songs_streamed, minsCutoff)
        if not ascending:
            list.sort(key=lambda song: song.total_ms_played, reverse=True)
        return list
    
    def getSortedPodcastStreamingHistory(self, minsCutoff = 30) -> list[Song]:
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

    def compareStreamedSongs(self, other:Self, min_mins_cutoff = 20) -> list[tuple[Song, Song]]:
        if not isinstance(other, SpotifyUser):
            return AssertionError('other must be an instance of SpotifyUser')
        
        MS_CUTOFF = (min_mins_cutoff * 60 * 1000)
        
        my_list = [song for song in self.songs_streamed.values() if song.total_ms_played > MS_CUTOFF]
        other_list = [song for song in other.songs_streamed.values() if song.total_ms_played > MS_CUTOFF]


        
        list1 = self.getSortedSongStreamingHistory(min_mins_cutoff)
        list2 = other.getSortedSongStreamingHistory(min_mins_cutoff)
        shared_songs: list[tuple[Song, Song]] = []
        
        for song1 in list1:
            for i in range(len(list2)):
                if song1 == list2[i]:
                    shared_songs.append((song1, list2[i]))

        return shared_songs

    def getLostSongCandidates(self, min_mins_listened=20) -> list[Song]:
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

