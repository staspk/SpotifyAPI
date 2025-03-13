import json, time, requests
from typing import Self, Union
from kozubenko.env import Env
from kozubenko.utils import *
from spotify_api.interfaces import *
from spotify_api.models import PlaylistId
from spotify_models import Song

    

class SimpleRequests:

    def _get(endpoint, access_token):
        pass

    def get_user_id(access_token = None) -> str:
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

    def get_playlist(playlist_id:str, access_token:str):
        """
        https://developer.spotify.com/documentation/web-api/reference/get-playlist
        """
        
        endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url=endpoint, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')
    
    def get_user_playlists(access_token:str):
        """
        https://developer.spotify.com/documentation/web-api/reference/get-a-list-of-current-users-playlists
        """

        endpoint = 'https://api.spotify.com/v1/me/playlists'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url=endpoint, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')


class CreatePlaylistRequest(IHandleRequest):
    """
    See: https://developer.spotify.com/documentation/web-api/reference/create-playlist
    """
    
    def __init__(self, user_id:str, access_token:str, playlist_name = 'Playlist1', public = True, description = ''):
        super().__init__()
        self.id: PlaylistId = None
        self.user_id = user_id
        self.access_token = access_token
        self.playlist_name = playlist_name
        self.description = description
        self.public = public
    
    def Handle(self) -> Self:
        """
        After Handle() is executed:\n
        `self.result == (PlaylistId | None)`\n
        `self.errorMsg set if self.result == None`
        """
        response = requests.post(
            url = f'https://api.spotify.com/v1/users/{self.user_id}/playlists',
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            },
            json = {
                'name': self.playlist_name,
                'description': self.description,
                'public': self.public
            }
        )

        if response.status_code == 201:
            data = response.json()
            self.id = PlaylistId(data.get('id'))
            self.result = self.id
        else:
            self.errorMsg = ErrorMsg(f'response.status_code: {response.status_code}\n{response.json().get('error').get('message')}')

        return self

    def Result(self, print=False) -> Union[PlaylistId, ErrorMsg]:
        if self.id is not None:
            if print:
                print_green(f'CreatePlaylistRequest Executed Successfully. PlaylistId: {self.id}')
            return self.id
        else:
            if print:
                print_red('CreatePlaylistRequest Failure:')
                print_red(self.errorMsg)
            return self.errorMsg

class SaveToPlaylistRequest(IHandleRequest):
    """
    Create Request Object with static constructors:
    - New_Playlist()
    - Existing_Playlist()

    Implements IHandleRequest:
    - Handle()
    - Result()

    See: https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
    """
 
    @staticmethod
    def New_Playlist(user_id:str, access_token:str, playlist_name:str, description = '') -> "SaveToPlaylistRequest":
        result = CreatePlaylistRequest(user_id, access_token, playlist_name, True, description).Handle().Result()
        if type(result) is PlaylistId:
            request = SaveToPlaylistRequest()
            request.playlistId = result
            request.user_id = user_id
            request.access_token = access_token
            request.playlist_name = playlist_name
            return request
        else:
            raise RuntimeError(f'Cannot continue due to error:\n{result.message}')

    @staticmethod
    def Existing_Playlist(id:Union[str, PlaylistId], access_token) -> "SaveToPlaylistRequest":
        if not isinstance(id, str) and not isinstance(id, PlaylistId):
            raise AssertionError('Exising_Playlist Id enforced type: str | PlaylistId')
        
        if isinstance(id, str):
            id = PlaylistId(id)

        response = requests.get(                                            # Checking if playlist exists / access_token is legal
            url=f'https://api.spotify.com/v1/playlists/{id}',
            headers = { 'Authorization': f'Bearer {access_token}' }
        )

        if response.status_code != 200:
            raise RuntimeError('Playlist not found')
        else:
            request = SaveToPlaylistRequest()
            request.playlistId = id
            request.access_token = access_token
            return request


    def _handle_chunk(self, uris:list, position:int) -> Union[Success, ErrorMsg]:
        response = requests.post(
            url = f'https://api.spotify.com/v1/playlists/{self.playlistId}/tracks',
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            },
            json = {
                'uris': uris,
                'position': position
            }
        )

        if response.status_code == 201:
            return Success()
        else:
            return ErrorMsg(f'response.status_code: {response.status_code}\n{response.json().get('error').get('message')}')

    def Handle(self, playlist: list[Song], position = 0) -> Self:
        """
        After Handle() is executed:\n
        `self.result == (Success | PartialSuccess | None)`\n
        `self.errorMsg set when self.result == (PartialSuccess | None)`
        """
        song_count = len(playlist)
        
        if song_count == 0:
            self.errorMsg = ErrorMsg('playlist passed into SaveToPlaylistRequest.Handle() has no songs')
            return
        
        CHUNK = 90
        requests_complete = 0
        total_requests_to_complete = (int)(song_count / CHUNK)
        last_request_chunk = song_count % 90

        for requests_complete in range(total_requests_to_complete):
            lower_bound = requests_complete * CHUNK
            upper_bound = lower_bound + CHUNK
            uris = [song.uri for song in playlist[lower_bound:upper_bound]]
            result = self._handle_chunk(uris, position + (CHUNK * requests_complete))

            if type(result) is ErrorMsg:
                self.errorMsg = result
                if requests_complete > 0:
                    self.result = PartialSuccess(f'Partial Success:\n{requests_complete * CHUNK} songs added to {self.playlist_name} [{self.playlistId}]') 
                return self
            
            time.sleep(1)
            
        if last_request_chunk > 0:
            lower_bound = song_count - last_request_chunk
            uris = [song.uri for song in playlist[lower_bound:]]
            result = self._handle_chunk(uris, lower_bound)

            if type(result) is Success:
                self.result = Success
            elif type(result) is ErrorMsg:
                self.result = PartialSuccess(f'Partial Success:\n{requests_complete * CHUNK} songs added to {self.playlist_name} [{self.playlistId}]')
                self.errorMsg = result

        return self
    
    def Result(self, print=False) -> Union[Success, PartialSuccess, ErrorMsg]:
        if self.result:
            success_type = type(self.result)
            if print:
                if success_type is Success:
                    print_green(f'SaveToPlaylistRequest Successful. {self.playlist_name} [{self.playlistId}]')
                elif success_type is PartialSuccess:
                    print_dark_yellow(self.result.description)
            return self.result
        
        else:
            if print:
                print_red('SaveToPlaylistRequest Failed:')
                print_red(self.errorMsg)
            return self.errorMsg