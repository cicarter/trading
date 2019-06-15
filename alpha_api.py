import requests
import json

def get_quote(sym):
    return json.loads(requests.get('https://www.alphavantage.co/query?'
                        'function=TIME_SERIES_INTRADAY&symbol=%s&interval=1min&apikey=XKQKT4UW4IG6LMYU' % sym).text)

print(get_quote('AAPL'))