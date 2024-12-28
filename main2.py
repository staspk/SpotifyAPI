# Stan = Spotify(r'Spotify_Data\Stan').getSortedSongStreamingHistory(1800)
# Luna = Spotify(r'Spotify_Data\Luna').getSortedSongStreamingHistory(1800)

# sharedSongs = Stan.compareSongsStreamed(Luna)
# Spotify.saveListToFile

# Spotify.saveListToFile(Stan, toFile=r'.\generated_data\Stan_Top_Streamed.txt')
# Spotify.saveListToFile(Luna, toFile=r'.\generated_data\Luna_Top_Streamed.txt')


# print(f'Stan Streamed: {len(Stan)}')
# print(f'Luna Streamed: {len(Luna)}')