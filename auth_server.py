from datetime import datetime, timedelta
import multiprocessing
import os
from pathlib import Path
import signal
import threading
import time

import requests, urllib, base64, json
from flask import Flask, redirect, request, jsonify

from kozubenko.env import Env
from kozubenko.timer import Timer
from kozubenko.utils import Utils


class LocalServerThread(threading.Thread):
    THREAD_NAME = 'LocalServerThread'
    PID = None

    def __init__(self, server, host = '127.0.0.1', port=8080):
        threading.Thread.__init__(self, name=LocalServerThread.THREAD_NAME)

        self.server = server
        self.host = host
        self.port = port

    def run(self):
        self.server.run(host=self.host, port=self.port)
        
    def stop(self):
        raise Exception('Server shutting down...')

def validate_token(reject = True) -> bool:
    if reject is True:
        return False
    Env.load()
    token_expiration_str = Env.vars.get('token_expiration', None)
    
    if not token_expiration_str:
        return False

    expiresOn = datetime.strptime(token_expiration_str, '%Y-%m-%d %H:%M')
    now = datetime.now()
    
    if now >= expiresOn:
        return False
    else:
        return True

def start_local_http_server():
    server = Flask(__name__)

    @server.route('/')
    def home():
        return '<div><a href="http://127.0.0.1:8080/login">LOGIN</a></div>'

    @server.route('/login')
    def login():
        params = {
            'response_type': 'code',
            'client_id': Env.vars['client_id'],
            'scope': Env.vars['scope'],
            'redirect_uri': Env.vars['redirect_uri'],
            'state': Utils.get_randomized_string(16)
        }
        
        return redirect('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params))

    @server.route('/callback')
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
            return jsonify({'error': 'Failed to get token'}), response.status_code
    
    @server.get('/shutdown')
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...'

    # global process
    thread = LocalServerThread(server)
    thread.start()
    # process = multiprocessing.Process(target=server.run('127.0.0.1', 8080), name=LocalServerThread.THREAD_NAME)
    # process.start()
    
    time.sleep(.1)

def request_token():
    return False

def stop_local_http_server():
    requests.get('http://127.0.0.1:8080/shutdown')
        



    
