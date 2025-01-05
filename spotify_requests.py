import requests
from kozubenko.env import Env
from spotify_models import Song 

class SpotifyRequests:

    @staticmethod
    def saveStreamingHistoryToSpotifyPlaylist(song_list:list[Song],
                                              user_id = 'staspk',
                                              playlist_name = 'Most Listened',
                                              description = 'A playlist generated with Spotify Extended Streaming History Data, see project at: https://github.com/staspk/Spotify-History'
                                             ):
        
        endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {Env.vars['access_token']}'
        }
        request_body = {
            'name': f'{playlist_name}',
            'description': f'{description}',
            'public': 'true'
        }

        response = requests.post(url=endpoint, headers=headers, data=request_body)
        print(f'response.status_code: {response.status_code}')

        if response.status_code == 201:         # Success code. Playlist has been created
            pass
        
        elif response.status_code == 401:       # Bad or expired token. Reauthenticate.
            pass

        elif response.status_code == 403:       # Bad OAuth request. Maybe check scopes?
            pass
        
        elif response.status_code == 429:       # The app has exceeded its rate limits
            pass