import threading
import logging
from wsgiref.simple_server import make_server

from flask import Flask

log = logging.getLogger(__name__)

class ServerThread(threading.Thread):
    THREAD_NAME = 'ServerThread'

    def __init__(self, app):
        threading.Thread.__init__(self, name=ServerThread.THREAD_NAME)
        self.server = make_server('127.0.0.1', 8080, app)
        ctx = app.app_context()
        ctx.push()

    def run(self):
        log.info('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def start_local_http_server():
    global server_thread

    app = Flask(__name__)

    # App routes defined here

    @app.route('/')
    def home():
        return 'Home'

    @app.route('/login')
    def login():
        return 'Login'

    @app.route('/callback')
    def callback():
        return 'Callback'

    server_thread = ServerThread(app)
    server_thread.start()
    print('Started ServerProcess, serving: http://127.0.0.1:8080')

def stop_local_http_server():
    server_thread.shutdown()

if __name__ == '__main__':
    import time

    start_local_http_server()

    time.sleep(10)  # I need more time to invoke an endpoint

    print('Terminating server.')
    stop_local_http_server()