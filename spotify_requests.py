class SpotifyRequests:
    def saveListToSpotifyPlaylist(playlist_name, song_list, user_id = 'staspk'):
        endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'