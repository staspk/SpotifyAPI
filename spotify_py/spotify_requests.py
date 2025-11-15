"""
response.status_code: 401
error message: The access token expired
"""
import time, requests
from typing import Self
from kozubenko.env import Env
from kozubenko.log import Log
from kozubenko.print import Print
from kozubenko.string import labeledStr
from kozubenko.utils import assert_list
from spotify_py import IHandleRequest
from spotify_py.spotify_auth import SpotifyAuth
from .ISong import ISong
from .IHandleRequest import *



class UserID(labeledStr):
    _user_id:UserID=None

    @staticmethod
    def Get() -> UserID:
        if(UserID._user_id is None):
            if not Env.loaded: Env.Load()
            user_id = Env.Vars.get('user_id', None)
            if(user_id is None): user_id = SimpleRequests.get_UserID()
        return user_id

class PlaylistID(labeledStr): pass
class PlaylistName(labeledStr): pass

class SimpleRequests:
    def get_UserID() -> UserID|None:
        """ https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
        """
        SpotifyAuth.Validate_Access_Token()
        response = requests.get(url='https://api.spotify.com/v1/me', headers={
            'Authorization': f'Bearer {Env.Vars['access_token']}'
        })

        if response.status_code == 200:
            user_id = UserID(response.json().get('id'))
            Env.Vars['user_id'] = user_id
            return user_id
        else:
            Log.Error(SimpleRequests, (
                f'response.status_code: {response.status_code}\n'
                f'error message: {response.json().get('error').get('message')}'
            ))

    def get_PlaylistName(playlist_id:str) -> PlaylistName|None:
        """ https://developer.spotify.com/documentation/web-api/reference/get-playlist
        """
        SpotifyAuth.Validate_Access_Token()
        response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers={
            'Authorization': f'Bearer {Env.Vars['access_token']}'
        })
        if response.status_code == 200:
            return response.json().get('id')
        
    def get_PlaylistID(playlist_name:str) -> PlaylistID|None:
        playlists = SimpleRequests.get_user_playlists()
        if type(playlists) is list:
            for playlist in playlists:
                if playlist['name'] == playlist_name:
                    return PlaylistID(playlist['id'])
        return None

    def get_user_playlists() -> list|None:
        """ https://developer.spotify.com/documentation/web-api/reference/get-a-list-of-current-users-playlists
        TODO: only capable of getting the first 50 playlists, rn
        """
        SpotifyAuth.Validate_Access_Token()
        response = requests.get('https://api.spotify.com/v1/me/playlists?limit=50', headers={
            'Authorization': f'Bearer {Env.Vars['access_token']}'
        })

        if response.status_code == 200:
            return response.json()['items']
        Log.Error(SimpleRequests, f'get_user_playlists()\nresponse.status_code: {response.status_code}\nerror message: {response.json().get('error').get('message')}')

    def create_playlist(playlist_name, description="", public=True) -> PlaylistID|str:
        """ https://developer.spotify.com/documentation/web-api/reference/create-playlist
        """
        SpotifyAuth.Validate_Access_Token()
        response = requests.post(f'https://api.spotify.com/v1/users/{UserID.Get()}/playlists',
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {Env.Vars['access_token']}'
            },
            json = {
                'name': playlist_name,
                'description': description,
                'public': public
            }
        )
        if response.status_code == 201:
            return PlaylistID(response.json().get('id'))
        error = f'response.status_code: {response.status_code}\n{response.json().get('error').get('message')}'
        Log.Error(SimpleRequests, error)
        return error

class SaveToPlaylistRequest(IHandleRequest):
    """
    See: https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist

    Example:
    ```python
    SaveToPlaylistRequest.New_Playlist(
        playlist_name='Her Favorite Songs',
        description='upper segment of her lifetime_listening_record - songs_I_already_liked'
    ).Handle(her_favorite_songs).Result()
    """

    def __init__(self, playlistID:PlaylistID=None, playlist_name:str=None):
        super().__init__()
        self.playlistID = playlistID
        self.playlist_name = playlist_name
    
    @classmethod
    def New_Playlist(cls, playlist_name:str, description = "", public=True) -> SaveToPlaylistRequest:
        result = SimpleRequests.create_playlist(playlist_name, description, public)
        if type(result) is PlaylistID:
            return SaveToPlaylistRequest(result, playlist_name)
        else: raise RuntimeError(f'SaveToPlaylistRequest.New_Playlist(): Cannot Continue. Error:\n{result}')

    @classmethod
    def Existing_Playlist(cls, identifier:str|PlaylistID) -> SaveToPlaylistRequest:
        """
        `identifier` - name of playlist or `PlaylistID`
        """
        if type(identifier) is PlaylistID: return SaveToPlaylistRequest(identifier, SimpleRequests.get_PlaylistName(identifier))
        if type(identifier) is str:
            request = SaveToPlaylistRequest(playlist_name=identifier)
            request.playlistID = SimpleRequests.get_PlaylistID(request.playlist_name)
            if request.playlistID is None:
                raise RuntimeError(f'SaveToPlaylistRequest: playlist could not be found with name: { request.playlist_name}')
            return request

    def Handle(self, playlist:list[ISong]) -> Self:
        """
        Spotify Web Api supports adding up to 100 songs per request.

        - `self.result` final value can be: `Success|PartialSuccess|Error`
        """
        assert_list('playlist', playlist, min_len=1)
        if not Env.loaded: Env.Load()

        CHUNK = 100
        song_count = len(playlist)
        requests_complete = 0
        total_requests_to_complete = (int)(song_count / CHUNK)
        last_request_chunk = song_count % 90

        result:True|str = None
        for requests_complete in range(total_requests_to_complete):
            lower_bound = requests_complete * CHUNK
            upper_bound = lower_bound + CHUNK
            result = self.handle_chunk([song.uri for song in playlist[lower_bound:upper_bound]])

            if result is not True:
                self.error = result
                if requests_complete > 0: self.result = Partial(f'{requests_complete*CHUNK}/{song_count} songs added to: {self.playlist_name} [{self.playlistID}]') 
                return self
            
            time.sleep(1)
            
        if last_request_chunk > 0:
            lower_bound = song_count - last_request_chunk
            uris = [song.uri for song in playlist[lower_bound:]]
            result = self.handle_chunk(uris)

            if result is not True:
                self.error = result
                if requests_complete > 0: self.result = Partial(f'{requests_complete*CHUNK}/{song_count} songs added to: {self.playlist_name} [{self.playlistID}]')
                else:                     self.result = Failure(f'0/{song_count} were added to: {self.playlist_name} [{self.playlistID}]')
                return self

        self.result = Success(f'{song_count}/{song_count} songs added to {self.playlist_name} [{self.playlistID}]')
        return self
    
    def handle_chunk(self, uris:list) -> True|str:
        """ returns `True` or an error message explaining what caused the failure """
        response = requests.post(f'https://api.spotify.com/v1/playlists/{self.playlistID}/tracks',
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {Env.Vars['access_token']}'
            },
            json = { 'uris': uris }
        )
        if response.status_code != 201:
            return f'response.status_code: {response.status_code}\n{response.json().get('error').get('message')}'
        return True

    def Result(self, print=True) -> Success|Partial|Failure:
        """ Tack onto the end of the Builder pattern chain to print the results of the `SaveToPlaylistRequest` """
        if print:
            match self.result:
                case Success(): Print.green(self.result)
                case Partial(): Print.dark_yellow(self.result)
                case Failure(): Print.red(self.result)
        return self.result
