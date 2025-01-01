import locale
import os, json
from pathlib import Path
from datetime import datetime
from spotify_models import ISong, IStreamed, Song, LikedSong, Podcast

class SpotifyUser:
    pathsToStreamingHistoryFiles:list = []
    pathToLikedSongs = None
    account_creation_time:datetime = None

    songs_streamed:    dict[str, Song]    = {}
    podcasts_streamed: dict[str, Podcast] = {}

    songsLiked: dict[str, LikedSong] = {}
    songDuplicates: dict[str, int] = {}

    def __init__(self, spotify_data_dir):
        for file in os.listdir(spotify_data_dir):
            if file == 'Spotify Extended Streaming History' or file == 'Spotify_Extended_Streaming_History':    # double-check that this is the default name of folder when downloaded from Spotify
                extended_streaming_history_dir = os.path.join(spotify_data_dir, file)
                for file_name in os.listdir(extended_streaming_history_dir):
                    if 'Streaming_History_Audio' in file_name:
                        self.pathsToStreamingHistoryFiles.append(os.path.join(extended_streaming_history_dir, file_name))

            if file == 'Spotify Account Data' or file == 'Spotify_Account_Data':        # double-check that this is the default name of folder when downloaded from Spotify
                # print('green')
                spotify_account_data_dir = os.path.join(spotify_data_dir, file)
                for file_name in spotify_account_data_dir:
                    if file_name == 'YourLibrary.json':
                        self.pathToLikedSongs = os.path.join(spotify_account_data_dir, file_name)
                    if file_name == 'Userdata.json':
                        userData = os.path.join(spotify_account_data_dir, file_name)
                        with open(userData, 'r') as json_file:
                            data = json.load(json_file)
                            self.account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")

        if self.pathsToStreamingHistoryFiles:
            self.parseStreamingHistory()
        if self.pathToLikedSongs:
            self.parseLikedSongs()

    def parseStreamingHistory(self):
        recordsIterated = 0
        for file in self.pathsToStreamingHistoryFiles:
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
                        print(f"Garbage Data at Record Read Cycle: {recordsIterated}")

                    else:
                        print(f"RuntimeError Reached on Cycle: {recordsIterated}")
                        raise RuntimeError('Neither Song nor Podcast')
                    
                    recordsIterated += 1
        print(f'parseStreamingHistory() iterated through: {recordsIterated} records.')

    def parseLikedSongs(self):
        with open(self.pathToLikedSongs, 'r', encoding='utf8') as file:
            data = json.load(file)
            for record in data['tracks']:
                song = LikedSong(record['track'], record['artist'], record['album'])

                fromLiked = self.songsLiked.get(repr(song), None)
                if fromLiked is None:
                    self.songsLiked[repr(song)] = song
                else:
                    numOfDuplicates = self.songDuplicates.pop(repr(song), 0)
                    self.songDuplicates[repr(song)] = (numOfDuplicates + 1)

    @staticmethod 
    def _getSortedList(dictInQuestion, minsCutoff) -> list:
        toReturnList = []
        msCutoff = (minsCutoff * 60 * 1000)

        for song in dictInQuestion.values():
            if song.total_ms_played > msCutoff:
                toReturnList.append(song)

        toReturnList.sort()
        # print(f'Sorting done in _getSortedList(). toReturnList Count: {len(toReturnList)}')
        return toReturnList

    def getSortedSongStreamingHistory(self, minsCutoff = 30) -> list:
        return SpotifyUser._getSortedList(self.songs_streamed, minsCutoff)
    
    def getSortedPodcastStreamingHistory(self, minsCutoff = 30) -> list:
        return SpotifyUser._getSortedList(self.podcasts_streamed, minsCutoff)
    


    def compareSongsStreamed(self, other):
        if not isinstance(other, SpotifyUser):
            return AssertionError('other must be an instance of Spotify')
        
        keys1 = self.songs_streamed.keys()
        keys2 = other.songs_streamed.keys()
        sharedKeys: list[Song, Song] = []
        
        for key in keys1:
            if keys2.__contains__(key):
                sharedKeys.append(self.songs_streamed[key], other.songs_streamed[key])

        return sharedKeys

    def getLostSongCandidates(self, minsCutoff=10) -> list:
        if len(self.songs_streamed) == 0:
            raise AssertionError('Can only call SpotifyUser.getLostSongCandidates() if Spotify has been fed the "Spotify Extended Streaming History" json data.')
        
        msCutoff = (minsCutoff * 60 * 1000)
        songsStreamedCopy = {}

        for song in self.songs_streamed.values():
            if song.total_ms_played > msCutoff:
                songsStreamedCopy[repr(song)] = song

        if len(self.songsLiked) > 0:
            for song in self.songsLiked.values():
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



