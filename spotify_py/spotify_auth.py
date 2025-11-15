import base64, urllib, requests, socketserver, http.server, threading
from datetime import datetime, timedelta
from kozubenko.print import ANSI, Print, Write
from kozubenko.html import Html
from kozubenko.http import Http
from kozubenko.url import Url
from kozubenko.OAuth2 import OAuth2
from kozubenko.env import Env
from definitions import REDIRECT_URI, PERMISSION_SCOPES


class SpotifyAuth(threading.Thread):
    """
    Using the `Spotify Web API` (creating playlists, etc.) requires an `access_token`  

        for further details, see: `SpotifyOAuth.Validate_Access_Token()`
    """
    redirect_uri = REDIRECT_URI
    scopes_needed = PERMISSION_SCOPES

    IP, PORT = "127.0.0.1", 8080
    Instance = None

    auth_code_flow_started, auth_code_flow_complete = False, False

    def Validate_Access_Token(reject=False):
        """
        On first call, procures an `access_token` via `authorization_code_flow()`
            - must login into Spotify/grant permissions (through a console generated link)
            - Required: `client_id`, `client_secret` key/value pairs in `.env`

        OR refreshes an existing token via a POST call (tokens have a 1hr lifespan)  

        `reject` - set True, if brand new `access_token` is desired, no matter what
        """
        if not Env.loaded: Env.Load()
        access_token = Env.Vars.get('access_token', None)
        refresh_token = Env.Vars.get('refresh_token', None)
        token_expiration_str = Env.Vars.get('token_expiration', None)

        if not (access_token and refresh_token and token_expiration_str) or reject is True:
            SpotifyAuth.authorization_code_flow(); return
        
        expiration = datetime.strptime(token_expiration_str, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=5)
        if datetime.now() > expiration:
            if not SpotifyAuth.refresh_token():
                SpotifyAuth.authorization_code_flow()

    def __init__(self, IP=IP, PORT=PORT):
        if(IP): SpotifyAuth.IP = IP
        if(PORT): SpotifyAuth.PORT = PORT
        threading.Thread.__init__(self, name='SpotifyAuth_thread', daemon=True)
        SpotifyAuth.Instance = self

    def stop(message=False):
        if SpotifyAuth.Instance is not None:
            SpotifyAuth.Instance.http_daemon.shutdown()
            SpotifyAuth.Instance = None

    def run(self):
        """ `threading.Thread` override, is the unit of work """
        with socketserver.TCPServer((SpotifyAuth.IP, SpotifyAuth.PORT), Server) as http_daemon:
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
            Print.dark_red(f'SpotifyAuth.refresh_token(): POST error, status_code: {response.status_code}')
            return False

    def authorization_code_flow():
        """
        Generates link that starts the `access_token` procurement process, and waits for user. Actual process handled by `Server`.
        """
        SpotifyAuth().start()
        endpoint = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode({
            'response_type': 'code',
            'client_id': Env.Vars['client_id'],
            'scope': SpotifyAuth.scopes_needed,
            'redirect_uri': SpotifyAuth.redirect_uri,
            'state': OAuth2.generate_state(),
            'show_dialog': True
        })

        SpotifyAuth.auth_code_flow_started = True

        Write.lite_red('\nNeed Permissions Grant through Spotify.'); Write.lite_green(' Please Login '); Print.lite_red('using this link:')
        Print.dark_gray(f'  {endpoint}')
        input(f'{ANSI.LITE_RED.value}\n  When redirected to success page, {ANSI.LITE_GREEN.value}Press Enter {ANSI.LITE_RED.value}to continue...\033[0m')

        if(SpotifyAuth.auth_code_flow_started and SpotifyAuth.auth_code_flow_complete):
            Print.green('\n  SpotifyAuth.authorization_code_flow(): Access Token Granted!\n')
        else: Print.dark_red('\n  SpotifyAuth.authorization_code_flow(): Process Not Complete! Expect Errors attempting to use the Spotify Web Api.\n')
        
        threading.Thread(target=SpotifyAuth.stop, daemon=True).start()
        
class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = Url(self.path)
        if url.pathname == '/callback':
            code  = url.params.get('code', [None])[0]
            state = url.params.get('state', [None])[0]  # in the future can be used to protect against cross-site request forgery

            if not (code and state):
                Http.handle_get(self, Html.Error().encode()); return

            url = 'https://accounts.spotify.com/api/token'
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + base64.b64encode(f'{Env.Vars.get('client_id', None)}:{Env.Vars.get('client_secret', None)}'.encode()).decode('utf-8')
            }
            data = {
                'code': code,
                'redirect_uri': SpotifyAuth.redirect_uri,
                'grant_type': 'authorization_code'
            }

            response = requests.post(url, headers=headers, data=data, json=True)
            if response.status_code == 200:
                SpotifyAuth.auth_code_flow_complete = True
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
    
    def log_message(self, format, *args):
        """ `SimpleHTTPRequestHandler` override to silence console output """
        pass
