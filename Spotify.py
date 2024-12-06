import os, json
from pathlib import Path
from Song import Song, LikedSong

def getSortedSongHistory(msCutoff = 0, returnDict = False):
    dir = r'.\Spotify_Data\Spotify_Extended_Streaming_History'
    jsons = [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith('json') and 'Streaming_History_Audio' in file]

    songs = {}

    for _json in jsons:
        with open(_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for record in data:
                song = Song(title=record['master_metadata_track_name'], artist=record['master_metadata_album_artist_name'], album=record['master_metadata_album_album_name'],
                            amount_played=1, amount_listened=0, total_ms_played=record['ms_played'], ts=[ list(record['ts']) ])
                
                if record.get('reason_end') == 'trackdone':
                    song.amount_listened = 1

                songInDict = songs.pop(repr(song), None)
                if songInDict is None:
                    songs[repr(song)] = song
                else:
                    song.amount_played += songInDict.amount_played
                    song.amount_listened += songInDict.amount_listened
                    song.total_ms_played += songInDict.total_ms_played
                    song.ts.extend(song.ts)
                    songs[repr(song)] = song

                if song.total_ms_played <= msCutoff:
                    songs.pop(repr(song))
                    # print(f'Song Removed due to Cutoff: {repr(song)}')
    
    if returnDict is True:
        return songs

    songList = list(songs.values())
    songList.sort()

    return songList

def getLikedSongs():
    jsonFile = r'.\Spotify_Data\Spotify_Account_Data\YourLibrary.json'

    likedSongs = {}

    with open(jsonFile, 'r', encoding='utf8') as file:
        data = json.load(file)
        for record in data['tracks']:
            song = LikedSong(record['track'], record['artist'])

            occurences = likedSongs.pop(repr(song), None)
            if occurences is None:
                likedSongs[repr(song)] = 1
            else:
                likedSongs[repr(song)] = (occurences + 1)
            
    list = []
    for likedSong in likedSongs.keys():
        song = likedSong.split(':')
        list.append(LikedSong(song[0], song[1]))

    return list

def saveSongListToFile(list, toFile=r'.\out.txt'):
    with open(rf'{toFile}', 'w', encoding='utf-8') as file:
        for song in list:
            file.write(str(song))
            file.write('\n\n')

def getLostSongCandidateFile(msCutoff=500000, toFile=r'.\lost_song_candidates.txt'):
    songHistory = getSortedSongHistory(msCutoff, returnDict=True)
    likedSongs = getLikedSongs()

    for likedSong in likedSongs:
        song = songHistory.pop(repr(likedSong), None)

    candidateList = list(songHistory.values())
    candidateList.sort()

    saveSongListToFile(candidateList, toFile)


