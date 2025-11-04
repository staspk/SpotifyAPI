from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

import requests, urllib, base64, json
from flask import Flask, redirect, request, jsonify
# from werkzeug.serving import make_server
from wsgiref.simple_server import make_server

from kozubenko.oauth2 import OAuth2
from kozubenko.env import Env


"""
Currently leaving this copy to work on it in the future. See LocalsServerThread.shutdown() for details
"""
class LocalServerThread(threading.Thread):
    THREAD_NAME = 'LocalServerThread'        

    def __init__(self, app: Flask):     
        threading.Thread.__init__(self, name=LocalServerThread.THREAD_NAME, daemon=True)

        self.server = make_server('127.0.0.1', '8080', app=app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()
    
    def shutdown(self):
        """
        Currently only works if the server has handled zero requests. If even one request has been handled, when the natural end of your console program comes,
        it will hang for 90-300 seconds, before letting the Program finally end. You will be locked up until then. Ctrl-c, Ctrl-x will not force-end it either.
        Have to kill the task either through Task Manager/powershell script.

        One workaround is setting daemon=True. Server will die on Program end. The drawback: even when you move on to do other unrelated things in the Program,
        your server will still be running in the background. Feels wrong, as it's using unecessary resources.

        I have moved on to a multiprocessing version of the code for the time being. I still want to get this to work in the future.
        """
        print(f'In LocalServerThread.shutdown(). Current Thread: {threading.current_thread().name}')
        self.server.shutdown()
        

def validate_token():
    Env.load()
    token_expiration_str = Env.vars.get('token_expiration', None)
    
    if token_expiration_str is None:
        request_token()
        return

    expiration = datetime.strptime(token_expiration_str, '%Y-%m-%d %H:%M')
    now = datetime.now()
    
    if now > expiration - timedelta(minutes=3):
        refresh_token()

def request_token():
    raise RuntimeError('request_token() currently not implemented')
    start_local_http_server()

    params = {
        'response_type': 'code',
        'client_id': Env.vars['client_id'],
        'scope': Env.vars['scope'],
        'redirect_uri': Env.vars['redirect_uri'],
        'state': OAuth2.generate_state()
    }

    requests.post('http://127.0.0.1:8080/login', params=params)

    return False



def start_local_http_server():
    for thread in threading.enumerate():
        if thread.name == LocalServerThread.THREAD_NAME:
            return
    
    app = Flask(__name__)

    @app.route('/')
    def home():
        return '<div><a href="http://127.0.0.1:8080/login">LOGIN</a></div>'

    @app.route('/login')
    def login():
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

    global local_server
    local_server = LocalServerThread(app)
    local_server.start()
    print(fr'Started {LocalServerThread.THREAD_NAME}, serving: http://127.0.0.1:8080')
    
    time.sleep(.1)

# Currently only works if the server has handled zero requests. Otherwise hangs 90-300 seconds before relinquishing control back to the Main Thread.
# After being stuck for a week, setting daemon=True and just letting the server run indefinitely until program exit.
def stop_local_http_server():
    local_server.shutdown()