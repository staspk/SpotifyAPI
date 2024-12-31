import os
from pathlib import Path
import requests, urllib, base64
import json
from flask import Flask, redirect, request, jsonify
from kozubenko.env import Env
from kozubenko.utils import Utils


Env.load()
app = Flask(__name__)

@app.route('/')
def home():
    return '<div><a href="http://127.0.0.1:8080/login">LOGIN</a></div>'

@app.route('/login')
def login():
    Env.add('state', Utils.get_randomized_string(16))

    params= {
        'response_type': 'code',
        'client_id': Env.vars['client_id'],
        'scope': Env.vars['scope'],
        'redirect_uri': Env.vars['redirect_uri'],
        'state': Env.vars['state']
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

        # token_info

        env_dir = r'.\.env'
        Path(env_dir).mkdir(parents=True, exist_ok=True)

        with open(fr'{env_dir}\spotify_auth_token.json', 'w') as json_file:
            json.dump(token_info, json_file)
        
        with open(fr'{env_dir}\spotify_auth_token_readable.json', 'w') as json_file:
            json.dump(token_info, json_file, indent=4)

        return jsonify(token_info)
    else:
        return jsonify({'error': 'Failed to get token'}), response.status_code

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)