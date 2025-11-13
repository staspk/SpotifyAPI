import urllib


class Url():
    """
    QoL for http servers

    Example:  
    ```python
    class Server(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            url = Url(self.path)
            pathname = url.pathname
            param1 = url.params.get('param1', [None])[0]
            param2 = url.params.get('param2', [None])[0]
    """
    def __init__(self, path):
        self.parsed = urllib.parse.urlparse(path)
        self.pathname = self.parsed.path
        self.params = urllib.parse.parse_qs(self.parsed.query)

    def pathname(self) -> str:
        """
        `http://127.0.0.1:8080/callback?code=AQDYLH` would return `/callback`
        """
        return self.pathname