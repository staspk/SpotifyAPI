import base64, urllib, requests, socketserver, http.server, threading
from datetime import datetime, timedelta
from kozubenko.print import ANSI, Print, Write
from kozubenko.html import Html
from kozubenko.http import Http
from kozubenko.url import Url
from kozubenko.OAuth2 import OAuth2
from kozubenko.env import Env


class SpotifyOAuth(threading.Thread):
    """
    Using the `Spotify Web API` (creating playlists, etc.) requires an `access_token`  

    `SpotifyOAuth.Validate_Access_Token()` the only call you need.
    """
    redirect_uri = 'http://127.0.0.1:8080/callback'
    scopes_needed = 'playlist-read-private playlist-read-collaborative user-library-read user-library-modify playlist-modify-public user-top-read'

    IP, PORT = "127.0.0.1", 8080
    Instance = None

    def Validate_Access_Token(reject=False):
        """
        Either procures an `access_token` (will ask user to login into Spotify/grant permissions)  
        or simply refreshes an existing token via a POST call.
        """
        Env.Load()
        access_token = Env.Vars.get('access_token', None)
        refresh_token = Env.Vars.get('refresh_token', None)
        token_expiration_str = Env.Vars.get('token_expiration', None)

        if not (access_token and refresh_token and token_expiration_str) or reject is True:
            SpotifyOAuth.spotify_authorization_code_flow(); return
        
        expiration = datetime.strptime(token_expiration_str, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=5)
        if datetime.now() > expiration:
            if not SpotifyOAuth.refresh_token():
                SpotifyOAuth.spotify_authorization_code_flow()

    def __init__(self, IP=IP, PORT=PORT):
        if(IP): SpotifyOAuth.IP = IP
        if(PORT): SpotifyOAuth.PORT = PORT
        threading.Thread.__init__(self, name='AuthServer_thread', daemon=True)
        SpotifyOAuth.Instance = self

    def stop(message=False):
        if SpotifyOAuth.Instance is not None:
            SpotifyOAuth.Instance.http_daemon.shutdown()
            SpotifyOAuth.Instance = None
            if(message): Print.green('AuthServer Stopped!')

    def run(self):
        """ `threading.Thread` override, is the unit of work """
        with socketserver.TCPServer((SpotifyOAuth.IP, SpotifyOAuth.PORT), Server) as http_daemon:
            self.http_daemon = http_daemon
            http_daemon.serve_forever(poll_interval=.5)

    def refresh_token() -> bool:
        Env.Load()
        refresh_token = Env.Vars.get('refresh_token', None)

        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(f'{Env.Vars['client_id']}:{Env.Vars['client_secret']}'.encode()).decode('utf-8')
        }
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            data = response.json()
            expiration = datetime.now() + timedelta(seconds=int(data['expires_in']))

            Env.Save('access_token', data['access_token'])
            Env.Save('token_expiration', expiration.strftime('%Y-%m-%d %H:%M:%S'))
            if 'refresh_token' in data: Env.Save('refresh_token', data['refresh_token'])
            return True
        else:
            Print.dark_red(f'AuthServer.refresh_token(): POST error, status_code: {response.status_code}')
            return False

    def spotify_authorization_code_flow():
        """  Generates link that starts the `access_token` procurement process, and waits for user. Actual process handled by `Server`. """
        SpotifyOAuth().start()
        endpoint = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode({
            'response_type': 'code',
            'client_id': Env.Vars['client_id'],
            'scope': SpotifyOAuth.scopes_needed,
            'redirect_uri': SpotifyOAuth.redirect_uri,
            'state': OAuth2.generate_state(),
            'show_dialog': True
        })

        Write.lite_red('\nNeed Permissions Grant through Spotify.'); Write.lite_green(' Please Login '); Print.lite_red('using this link:')
        Print.dark_gray(f'  {endpoint}')
        input(f'{ANSI.LITE_RED.value}\n  When redirected to success page, {ANSI.LITE_GREEN.value}Press Enter {ANSI.LITE_RED.value}to continue...\033[0m')

        access_token, refresh_token, token_expiration = Env.Vars.get('access_token', None), Env.Vars.get('refresh_token', None), Env.Vars.get('token_expiration', None)
        if not(access_token and refresh_token and token_expiration):
            Print.dark_red('\nAuthServer.spotify_authorization_code_flow(): Process Not Complete! Expect Errors attempting to use the Spotify WebApi.\n')
        SpotifyOAuth.stop()
        
class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = Url(self.path)
        if url.pathname == '/callback':
            code  = url.params.get('code', [None])[0]
            state = url.params.get('state', [None])[0]  # in the future can be used to protect against cross-site request forgery

            if not (code and state):
                return

            url = 'https://accounts.spotify.com/api/token'
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + base64.b64encode(f'{Env.Vars.get('client_id', None)}:{Env.Vars.get('client_secret', None)}'.encode()).decode('utf-8')
            }
            data = {
                'code': code,
                'redirect_uri': SpotifyOAuth.redirect_uri,
                'grant_type': 'authorization_code'
            }

            response = requests.post(url, headers=headers, data=data, json=True)
            if response.status_code == 200:
                data = response.json()
                expiration = datetime.now() + timedelta(seconds=int(data['expires_in']))
                Env.Save({
                    'access_token': data['access_token'],
                    'refresh_token': data['refresh_token'],
                    'token_expiration': expiration.strftime('%Y-%m-%d %H:%M:%S')
                })
                Http.handle_get(self, Html.Success().encode())
            else:
                Http.handle_get(self, Html.Error().encode())
        else: self.send_error(404, 'does not exist')
