"""
`auth_server.validate_token()`\n
`auth_server.print_help()`
"""
from datetime import datetime, timedelta
import multiprocessing
from pathlib import Path

import requests, urllib, base64, json
from flask import Flask, redirect, request, jsonify
from werkzeug.serving import make_server

from kozubenko.env import Env
from kozubenko.print import Print
from kozubenko.OAuth2 import OAuth2



def _server_worker():
    app = Flask(__name__)

    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/')
    def home():
        return '<div><a href="http://127.0.0.1:8080/login">LOGIN</a></div>'

    @app.route('/login')
    def login():
        Env.load()

        params = {
            'response_type': 'code',
            'client_id': Env.vars['client_id'],
            'scope': Env.vars['scope'],
            'redirect_uri': Env.vars['redirect_uri'],
            'state': OAuth2.generate_state()
        }
        
        return redirect('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params))

    @app.route('/callback')
    def callback():
        Env.load()

        code = request.args.get('code', None)
        state = request.args.get('state', None)

        if not state:
            return redirect('/#' + urllib.parse.urlencode({'error': 'state_mismatch'}))
        
        token_url = 'https://accounts.spotify.com/api/token'

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(f'{Env.vars['client_id']}:{Env.vars['client_secret']}'.encode()).decode('utf-8')
        }

        data = {
            'code': code,
            'redirect_uri': Env.vars['redirect_uri'],
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, headers=headers, data=data, json=True)
        timestamp = response.headers['date']

        if response.status_code == 200:
            token_info = response.json()

            env_dir = r'.\.env'
            Path(env_dir).mkdir(parents=True, exist_ok=True)

            with open(fr'{env_dir}\spotify_auth_token.json', 'w') as json_file:
                json.dump(token_info, json_file)
            
            with open(fr'{env_dir}\spotify_auth_token_readable.json', 'w') as json_file:
                json.dump(token_info, json_file, indent=4)

            Env.save('access_token', token_info['access_token'])
            Env.save('refresh_token', token_info['refresh_token'])
            token_expiration = datetime.now() + timedelta(seconds=int(token_info['expires_in']))
            Env.save('token_expiration', token_expiration.strftime('%Y-%m-%d %H:%M'))

            return jsonify(token_info)
        else:
            print(f'/CallBack endpoint hit. response.status_code == {response.status_code}')
            return jsonify({'error': 'Failed to get token'}), response.status_code
        
    server = make_server('127.0.0.1', 8080, app)
    ctx = app.app_context()
    ctx.push()

    server.serve_forever()

def start_local_http_server():
    global server_process
    server_process = multiprocessing.Process(target=_server_worker, name="LocalServerProcess")
    
    server_process.start()

def stop_local_http_server():
    server_process.terminate()
    server_process.join()

def validate_token(reject=False):
    """
    The only "public" function you need to get a Spotify Authorization Token.

    `if __name__ == '__main__':` guard clause required due to use of multi-processing
    """
    Env.load()
    token_expiration_str = Env.vars.get('token_expiration', None)
    
    if token_expiration_str is None or reject is True:
        _request_token()
        return

    expiration = datetime.strptime(token_expiration_str, '%Y-%m-%d %H:%M')
    now = datetime.now()
    
    if now > expiration - timedelta(minutes=3):
        _refresh_token()

def _request_token():
    start_local_http_server()

    Print.green('\nauth_server has spun up server for Spotify Authorization Code Flow.', False)
    Print.yellow(' Login here: http://127.0.0.1:8080')
    Print.green('  lost? call auth_server.print_help()')
    print()

    input(f'\033[93m  When redirected to success page, Press Enter to continue...\033[0m')

    stop_local_http_server()

def _refresh_token():
    Env.load()
    refresh_token = Env.vars.get('refresh_token', None)
    url = 'https://accounts.spotify.com/api/token'

    if not refresh_token:
        print('Found an expired token in .env, but refresh_token missing in .env file')
        print('Please re-run with auth_server.validate_token(reject=True) to get new Authorization Token')
        exit()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(f'{Env.vars['client_id']}:{Env.vars['client_secret']}'.encode()).decode('utf-8')
    }

    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        response_data = response.json()
        Env.save('access_token', response_data['access_token'])
        token_expiration = datetime.now() + timedelta(seconds=int(response_data['expires_in']))
        Env.save('token_expiration', token_expiration.strftime('%Y-%m-%d %H:%M'))
        if 'refresh_token' in response_data:
            Env.save('refresh_token', response_data['refresh_token'])
            Print.green('new refresh token saved to .env')
    else:
        RuntimeError(f'_refresh_token() not implemented for response.status_code == {response.status_code}.')

def print_help():
    Print.yellow('\nSpotify Authorization Code Flow -> ')
    Print.yellow('    Use auth_server.validate_token(). Required example .env file:')
    Print.gray('project_root/.env/.env:')
    Print.dark_gray(f'client_id=7b0acca87e49424190a5eee6c8a63fe9')
    Print.dark_gray('client_secret=f53b708a121e4e3da5aee75814c394ab')
    Print.dark_gray('scope=playlist-modify-public user-top-read user-library-read user-library-modify')
    Print.dark_gray(f'redirect_uri=http://127.0.0.1:8080/callback')
    print()
    Print.yellow('For more details, see: https://developer.spotify.com/documentation/web-api/tutorials/code-flow\n')
    print('\n')

