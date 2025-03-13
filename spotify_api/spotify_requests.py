from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import json
import pprint
from typing import Callable, Protocol, Self, Union
import requests
from kozubenko.env import Env
from kozubenko.utils import *
from spotify_api.IHandleRequest import ErrorMsg, IHandleRequest
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

    def __init__(self, user_id:str, access_token:str, playlist_name = 'Playlist1', public = True, description = ''):
        self.user_id = user_id
        self.access_token = access_token
        self.playlist_name = playlist_name
        self.description = description
        self.public = public
    
    def Handle(self) -> Self:
        endpoint = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'

        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        request_body = {
            'name': self.playlist_name,
            'description': self.description,
            'public': self.public
        }

        response = requests.post(url=endpoint, headers=headers, json=request_body)

        if response.status_code == 201:
            data = response.json()
            self.id = PlaylistId(data.get('id'))
            self.result = self.id.__str__
        else:
            self.errorMsg = f'response.status_code: {response.status_code}\n'
            self.errorMsg += f'{response.json().get('error').get('message')}'

        return self

    def Result(self, print=False) -> Union[PlaylistId, ErrorMsg]:
        if self.result is not None:
            if print:
                print_green(f'CreatePlaylistRequest Executed Successfully. PlaylistId: {self.id}')
            return self.result
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
    """

    Id: PlaylistId = None

    @staticmethod
    def New_Playlist(user_id:str, access_token:str, playlist_name:str, description = '') -> "SaveToPlaylistRequest":
        result = CreatePlaylistRequest(user_id, access_token, playlist_name, True, description).Handle().Result()
        if isinstance(result, ErrorMsg):
            raise RuntimeError(f'Cannot continue due to error:\n{result}')
        if isinstance(result, PlaylistId):
            request = SaveToPlaylistRequest()
            request.Id = result
            request.user_id = user_id
            request.access_token = access_token
            return request

    @staticmethod
    def Existing_Playlist(Id:Union[str, PlaylistId], access_token) -> "SaveToPlaylistRequest":
        if not isinstance(Id, str) and not isinstance(Id, PlaylistId):
            raise AssertionError('Exising_Playlist Id enforced type: str | PlaylistId')
        
        if isinstance(Id, str):
            Id = PlaylistId(Id)

        response = requests.get(                                            # Checking if playlist exists / access_token is legal
            url=f'https://api.spotify.com/v1/playlists/{Id}',
            headers = { 'Authorization': f'Bearer {access_token}' }
        )

        if response.status_code != 200:
            raise RuntimeError('Playlist not found')
        else:
            request = SaveToPlaylistRequest()
            request.Id = Id
            request.access_token = access_token
            return request

    def Handle(self, playlist: list[Song]) -> Self:
        uris = ''
        for song in playlist:
            uris += f'{song.uri} ,'
        uris = uris[:-2]

        response = requests.post(
            url = f'https://api.spotify.com/v1/playlists/{self.Id}/tracks',
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            },
            json = {
                'uris': uris,
                'position': 0
            }
        )
        
        if response.status_code == 201:
            self.result = 'Success'
        else:
            self.errorMsg = ErrorMsg(f'response.status_code: {response.status_code}')
            self.errorMsg.message += response.json().get('error').get('message')

        return self

        
    
    def Result(self, print=False) -> Union[str, ErrorMsg]:
        if self.result is not None:
            if print:
                print_green(f'SaveToPlaylistRequest Successful. PlaylistId: {self.Id}')
            return self.result
        else:
            if print:
                print_red('SaveToPlaylistRequest Failed.')
                print_red(self.errorMsg)
            return self.errorMsg