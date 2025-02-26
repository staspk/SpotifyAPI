import multiprocessing
import logging

from werkzeug.serving import make_server
from flask import Flask

log = logging.getLogger(__name__)

def worker():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'home'

    @app.route('/login')
    def login():
        return 'login'

    @app.route('/callback')
    def callback():
        return 'callback'

    server = make_server('127.0.0.1', 8080, app)
    ctx = app.app_context()
    ctx.push()

    log.info('starting server')
    server.serve_forever()

def start_local_http_server():
    global server_process

    server_process = multiprocessing.Process(target=worker, name="ServerProcess")
    server_process.start()
    print('Started ServerProcess, serving: http://127.0.0.1:8080')

def stop_local_http_server():
    server_process.terminate()

if __name__ == '__main__':
    import time

    start_local_http_server()

    time.sleep(10)  # I need more time to invoke an endpoint

    stop_local_http_server()