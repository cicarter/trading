from token_handler import TokenHandler
import datetime
import charts
from stock import Stock


th = TokenHandler()
tok = th.get_token()
th.save_token()

print('Token expires at: ', datetime.datetime.fromtimestamp(th.get_token_expiration_time()))

# TODO
"""
    Analysis class
    Paper trading class
    Scanner implementation
    Get real time stock data
"""


s = Stock('AAPL', load_data=False)
chart = charts.Charts(s, rt=True)
chart.show()
s.save_rt_data()
s.save_normal_data()


# drive_l2 = WebScraper('http://markets.cboe.com/us/equities/market_statistics/book/AAPL/')

