from Spotify import Spotify


songs = Spotify(r'Spotify_Data\Stan').getSortedSongStreamingHistory()

# for song in songs:
#     print(song)
#     print()

Spotify.saveListToFile(songs, toFile=r'.\Stan_top_streamed.txt')