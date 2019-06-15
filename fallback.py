from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
import ssl
import json

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        # Get the Auth Code
        path, _, query_string = self.path.partition('?')
        code = parse_qs(query_string)['code'][0]

        # Post Access Token Request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'authorization_code', 'access_type': 'offline', 'code': code,
                'client_id': 'CICARTER8080@AMER.OAUTHAP', 'redirect_uri': 'https://127.0.0.1:8080'}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)

        # returned just to test that it's working
        self.wfile.write(authReply.text.encode())


httpd = HTTPServer(('127.0.0.1', 8080), Handler)


# SSL cert
httpd.socket = ssl.wrap_socket(httpd.socket,
                               keyfile='/root/progects/stock/td_ameritrade/try2/key.pem',
                               certfile='/root/progects/stock/td_ameritrade/try2/certificate.pem', server_side=True)

httpd.serve_forever()