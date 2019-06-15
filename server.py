from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import ssl

class Handler(BaseHTTPRequestHandler):
    __code = ""

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        print("In this method")
        self._set_headers()
        auth_reply = 'This is a test'
        path, _, query_string = self.path.partition('?')
        try:
            Handler.__code = parse_qs(query_string)['code'][0]
        except Exception as e:
            pass
        print('Code is %s' % self.__code)
        # returned just to test that it's working
        self.wfile.write(auth_reply.encode())

    def get_code(self):
        return self.__code


    @staticmethod
    def open_window_auth():
        # httpd = HTTPServer(('127.0.0.1', 8080), Handler)
        # SSL cert
        # httpd.socket = ssl.wrap_socket(httpd.socket,
        #                                keyfile='/root/projects/stock/td_ameritrade/try2/key.pem',
        #                                certfile='/root/projects/stock/td_ameritrade/try2/certificate.pem',
        #                                server_side=True)

        # invoke https-authentication-page
        import webbrowser as web
        web.get('/usr/bin/chromium').open('https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A8080&'
                    'client_id=CICARTER8080%40AMER.OAUTHAP')


        httpd.handle_request()
        code = Handler.get_code(Handler)

        return code


httpd = HTTPServer(('127.0.0.1', 8080), Handler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                                keyfile='/root/projects/stock/td_ameritrade/try2/key.pem',
                                certfile='/root/projects/stock/td_ameritrade/try2/certificate.pem',
                                server_side=True)

