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




class SpotifyRequests():
    def __init__(self, user_id:str, access_token:str):
        self.user_id = user_id
        self.access_token = access_token

    def get_playlist(self, playlistId):
        response = requests.get(
            url=f'https://api.spotify.com/v1/playlists/{playlistId}',
            headers=self._authorized_header(),
        )

        if(response.status_code == 200):
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')

    def handle_response(response, onSuccess: Callable):
        if(response.status_code == 200):
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')
    
    def _get(endpoint, headers_authorized_header()):
        requests.get(url=endpoint, headers=)

    def _authorized_header(self):
        return { 'Authorization': f'Bearer {self.access_token}' }
    

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
        endpoint = 'https://api.spotify.com/v1/me/playlists'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(endpoint, headers)

        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')


    def saveStreamingHistoryToSpotifyPlaylist(
        song_list:list[Song],
        user_id = 'staspk',
        playlist_name = 'Most Listened',
        description = 'A playlist auto-generated with SpotifyApi, see project at: https://github.com/staspk/Spotify-History'
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
        else:
            print_red(f'response.status_code: {response.status_code}')
            print_red(f'error message: {response.json().get('error').get('message')}')

    

class CreatePlaylistRequest(IHandleRequest):
    result: PlaylistId = None

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
            self.result = PlaylistId(data.get('id'))
            print_green(f'Success. {self.playlist_name} created. Id: {self.result.Id}')
        else:
            self.ErrorMsg = f'response.status_code: {response.status_code}\n'
            self.ErrorMsg += f'{response.json().get('error').get('message')}'
            print_red(self.ErrorMsg)

        return self

    def Result(self) -> Union[PlaylistId, ErrorMsg]:
        if self.ErrorMsg is None:
            return self.result
        else:
            return None

class SaveToPlaylistRequest(IHandleRequest):
    """
    Create Request Object with static constructors:
    - New_Playlist()
    - Existing_Playlist()
    """

    Id: PlaylistId = None

    @staticmethod
    def New_Playlist(user_id, access_token, playlist_name) -> Self:
        request = SaveToPlaylistRequest()
        result = CreatePlaylistRequest(user_id, access_token, playlist_name, True).Handle().Result()
        if result is ErrorMsg:
            raise RuntimeError(f'Cannot continue due to error:\n{result}')
        if result is PlaylistId:
            request.Id = result
            return request

    @staticmethod
    def Existing_Playlist(Id: PlaylistId) -> Self:
        if not isinstance(Id, PlaylistId):
            raise ValueError('Exising_Playlist only takes a param of type PlaylistId')
        
        requests.post


        pass

    def Handle() -> Self:
        pass
        
    
    def Result() -> Self:
        pass

    # @staticmethod
    # def To_New_Playlist()

        

