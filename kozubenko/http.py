from http.server import SimpleHTTPRequestHandler


class Http():
    def handle_get(handler:SimpleHTTPRequestHandler, html):
        """
        QoL utility function for http servers

        Example:  
        ```python
        class Server(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if url.pathname == '/':        Http.handle_get(self, INDEX_HTML)
                if url.pathname == '/report':  Http.handle_get(self, REPORT_HTML)
        """
        handler.send_response(200)
        handler.send_header("Content-type", "text/html; charset=utf-8")
        handler.send_header("Content-Length", str(len(html)))
        handler.end_headers()
        handler.wfile.write(html)
