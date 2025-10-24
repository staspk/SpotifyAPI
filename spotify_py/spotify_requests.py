import json, time, requests
from typing import Self, Union
from kozubenko.env import Env
from kozubenko.print import *
from .ISong import ISong
from spotify_py.interfaces import *
from spotify_py.models import PlaylistId

    

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
    
    def get_user_playlists(access_token:str) -> Union[list, ErrorMsg]:
        """
        https://developer.spotify.com/documentation/web-api/reference/get-a-list-of-current-users-playlists
        """

        response = requests.get(
            url='https://api.spotify.com/v1/me/playlists?limit=50',
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
        )

        if response.status_code == 200:
            return response.json()['items']
        else:
            return ErrorMsg(f'response.status_code: {response.status_code}\nerror message: {response.json().get('error').get('message')}')

    def create_playlist(access_token:str, user_id:str, playlist_name:str, public:bool = True, description:str = '') -> Union[PlaylistId, ErrorMsg]:
        response = requests.post(
            url = f'https://api.spotify.com/v1/users/{user_id}/playlists',
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            json = {
                'name': playlist_name,
                'description': description,
                'public': public
            }
        )

        if response.status_code == 201:
            playlist_id:str = response.json().get('id')
            print(f'Playlist successfully created. Name: {playlist_name}. Id: {playlist_id}')
            return playlist_id
        else:
            return ErrorMsg(f'response.status_code: {response.status_code}\n{response.json().get('error').get('message')}')

    def find_playlist(access_token:str, identifier:str) -> Union[tuple, None]:
        """
        identifier is either:
        - name of playlist
        - playlistId
        """
        response = SimpleRequests.get_user_playlists(access_token)

        if type(identifier) is PlaylistId:
            identifier = identifier.id

        if type(response) is list:
            for playlist in response:
                if playlist['name'] == identifier or playlist['id'] == identifier:
                    return playlist
        return None

class CreatePlaylistRequest(IHandleRequest):
    """
    See: https://developer.spotify.com/documentation/web-api/reference/create-playlist
    """
    
    def __init__(self, access_token:str, user_id:str, playlist_name = 'Playlist1', public = True, description = ''):
        super().__init__()
        self.id: PlaylistId = None
        self.access_token = access_token
        self.user_id = user_id
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
    def New_Playlist(
        access_token:str,
        user_id:str,
        playlist_name:str,
        description = ''
    ) -> "SaveToPlaylistRequest":
        result = CreatePlaylistRequest(access_token, user_id, playlist_name, True, description).Handle().Result()
        if type(result) is PlaylistId:
            request = SaveToPlaylistRequest()
            request.playlistId = result
            request.access_token = access_token
            request.user_id = user_id
            request.playlist_name = playlist_name
            return request
        else:
            raise RuntimeError(f'Cannot continue due to error:\n{result.message}')

    @staticmethod
    def Existing_Playlist(access_token, identifier:Union[str, PlaylistId]) -> "SaveToPlaylistRequest":
        if type(identifier) not in (str, PlaylistId):
            raise RuntimeError('SaveToPlaylistRequest.Exising_Playlist(): identifier must be of type == (str | PlaylistId)')

        playlist = SimpleRequests.find_playlist(access_token, str(identifier))

        if playlist is None:
            raise RuntimeError(f'Playlist not found. {str(identifier)}')

        request = SaveToPlaylistRequest()
        request.access_token = access_token
        request.playlistId = PlaylistId(playlist['id'])
        request.playlist_name = playlist['name']
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

    def Handle(self, playlist: list[ISong], position = 0) -> Self:
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
                self.result = Success()
            elif type(result) is ErrorMsg:
                self.result = PartialSuccess(f'Partial Success:\n{requests_complete * CHUNK} songs added to {self.playlist_name} [{self.playlistId}]')
                self.errorMsg = result

        return self
    
    def Result(self, print=False) -> Union[Success, PartialSuccess, ErrorMsg]:
        if self.result:
            success_type = type(self.result)
            if print:
                if success_type is Success:
                    print_green(f'SaveToPlaylistRequest successful on: {self.playlist_name} [{self.playlistId}]')
                elif success_type is PartialSuccess:
                    print_dark_yellow(f'SaveToPlaylistRequest only partially successful.\n{self.result.description}')
            return self.result
        else:
            if print:
                print_red('SaveToPlaylistRequest Failed:')
                print_red(self.errorMsg)
            return self.errorMsg