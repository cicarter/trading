
import datetime
import json
import requests
import server

class TokenHandler:
    __token = None
    __refresh_token = ""

    # token_expiration_time is misleading it's always going to be 1800 ie 30 minutes
    __token_expiration_time = 0

    # refresh_token_expiration_time is misleading it's always going to be 1800 ie x minutes
    __refresh_token_expiration_time = 0
    __token_type = ""
    __token_gotten_time = 0

    def __init__(self):
        try:
            self.load_token()
        except IOError as e:
            print('Could not load tok.json', e)
            self.set_vars()

        if not self.check_token():
            print('Token timed out')
            if self.check_refresh_token():
                print('Using refresh token')
                self.grab_token_with_refresh()
            else:
                self.set_vars()

    def get_token(self):
        if self.check_token():
            return self.__token
        elif self.check_refresh_token():
            self.grab_token_with_refresh()
        else:
            self.set_vars()

    def get_refresh_token(self):
        return self.__refresh_token

    def get_token_expiration_time(self):
        return self.__token_gotten_time + self.__token_expiration_time

    def get_refresh_token_expiration_time(self):
        return self.__token_gotten_time + self.__refresh_token_expiration_time

    def get_token_type(self):
        return self.__token_type

    def get_token_got_time(self):
        return self.__token_gotten_time

    def set_vars(self):
        try:
            print('No usable token found fetching new one')
            code_entered = server.Handler.open_window_auth()
            self.__token_gotten_time = datetime.datetime.now().timestamp()
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'grant_type': 'authorization_code', 'access_type': 'offline', 'code': code_entered,
                    'client_id': 'CICARTER8080@AMER.OAUTHAP', 'redirect_uri': 'https://127.0.0.1:8080'}
            response = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
            testing = json.loads(response.text)
            self.__token = testing['access_token']
            self.__refresh_token = testing['refresh_token']
            self.__token_expiration_time = testing['expires_in']
            self.__refresh_token_expiration_time = testing['refresh_token_expires_in']
            self.__token_type = testing['token_type']
            print(self)
        except Exception as e:
            print(e)
            input('Enter something to continue')

    def save_token(self):
        save = {'Token': self.__token, 'Refresh_Token': self.__refresh_token,
                'Token_False_Exp_Time': self.__token_expiration_time,
                'RTET': self.__refresh_token_expiration_time, 'Token_Type': self.__token_type,
                'Token_Gotten_Time': self.__token_gotten_time, 'Refresh_Expires': self.__refresh_token_expiration_time}

        with open('tok.json', 'w') as out:
            json.dump(save, out)

    def load_token(self):
        print('loading token')
        try:
            with open('tok.json', 'r') as in_put:
                token = json.load(in_put)
            self.__token = token['Token']
            self.__refresh_token = token['Refresh_Token']
            self.__token_expiration_time = token['Token_False_Exp_Time']
            self.__token_type = token['Token_Type']
            self.__token_gotten_time = token['Token_Gotten_Time']
            self.__refresh_token_expiration_time = token['Refresh_Expires']

            self.get_token()
            return True

        except KeyError as e:
            print(e)
            self.set_vars()
            return False

    def check_token(self):
        time_now = datetime.datetime.now().timestamp()
        test_time = self.get_token_expiration_time()

        if time_now < test_time:
            return True
        else:
            return False

    def check_refresh_token(self):
        time_now = datetime.datetime.now().timestamp()
        test_time = self.get_refresh_token_expiration_time()

        if time_now < test_time:
            return True
        else:
            return False

    def grab_token_with_refresh(self):
        self.__token_gotten_time = datetime.datetime.now().timestamp()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'refresh_token', 'access_type': 'offline', 'refresh_token': self.__refresh_token,
                'client_id': 'CICARTER8080@AMER.OAUTHAP'}
        response = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        data = json.loads(response.text)
        print(data)
        try:
            self.__token = data['access_token']
            self.__refresh_token = data['refresh_token']
            self.__token_expiration_time = data['expires_in']
            self.__refresh_token_expiration_time = data['refresh_token_expires_in']
            self.__token_type = data['token_type']
        except KeyError as ke:
            print(ke)
