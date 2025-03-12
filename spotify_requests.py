import requests
from kozubenko.env import Env
from kozubenko.utils import print_green, print_red
from spotify_models import Song 

class SpotifyRequests:

    def get_user_id(access_token = None):
        endpoint = 'https://api.spotify.com/v1/me'

        if access_token is None:
            Env.load()
            access_token = Env.vars.get('access_token')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url=endpoint, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print_green(data.get('id'))
            return data.get('id')
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')


    def create_spotify_playlist(
        user_id = 'staspk',
        playlist_name = 'Playlist1',
        description = 'A playlist generated with Spotify Extended Streaming History Data, see project at: https://github.com/staspk/Spotify-History',
        public = True
    ):
        """
        Required: access_token in .env file
        """
        endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'

        Env.load()

        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {Env.vars.get('access_token')}'
        }
        request_body = {
            'name': playlist_name,
            'description': description,
            'public': public
        }

        response = requests.post(url=endpoint, headers=headers, data=request_body)

        if response.status_code < 400:
            



    def saveStreamingHistoryToSpotifyPlaylist(
        song_list:list[Song],
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