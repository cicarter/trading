import datetime
# from web_scrapper import WebScraper
import td_ameritrade_api as api
import json
import matplotlib.dates as mdates

class Stock:
    list_of_rt_vars = [
        'bidPrice',
        'bidSize',
        'askPrice',
        'askSize',
        'lastPrice',
        'lastSize',
        'openPrice',
        'highPrice',
        'lowPrice',
        'closePrice',
        'netChange',
        'totalVolume',
        'marginable',
        'volatility',
        'mark',
        'tradeTimeInLong'
    ]

    __symbol = ""
    __dates = []
    __high = []
    __low = []
    __open = []
    __close = []
    __volume = []

    __rt_data = []
    __rt_period = ''

    __my_l2_order_book = []

    __quote = {}
    __quote_high = ""
    __quote_low = ""

    __web_page_driver = ""

    def __init__(self, symbol, rt_per=2, load_data=False):
        self.__symbol = symbol
        if load_data:
            try:
                self.load_normal_data()
                self.load_rt_data()
            except IOError as e:
                print('Could not load in data from file', e)
                self.update_data(api.get_price_history_api('year', '1', 'daily', '1', 'true',
                                                           self.__symbol))
                self.__rt_period = rt_per
                self.add_rt_data()

        else:

            self.update_data(api.get_price_history_api('year', '1', 'daily', '1', 'true',
                                                       self.__symbol))

            self.__rt_period = rt_per
            self.add_rt_data()

        self.update_quote_data()

    def save_rt_data(self):
        with open('data_rt.json', 'w') as out:
            json.dump(self.__rt_data, out)

    def load_rt_data(self):
        with open('data_rt.json', 'r') as in_put:
            self.__rt_data = json.load(in_put)

    def save_normal_data(self):
        save = [self.__dates, self.__open, self.__high, self.__low, self.__close, self.__volume]
        with open('data_normal.json', 'w') as out:
            json.dump(save, out)

    def load_normal_data(self):
        with open('data_normal.json', 'r') as in_put:
            self.__dates, self.__open, self.__high, self.__low, self.__close, self.__volume = json.load(in_put)

    def get_symbol(self):
        return self.__symbol

    def get_dates(self):
        return self.__dates

    def get_highs(self):
        return self.__high

    def get_lows(self):
        return self.__low

    def get_opens(self):
        return self.__open

    def get_closes(self):
        return self.__close

    def get_volume(self):
        return self.__volume

    def get_rt_data(self):
        return self.__rt_data

    def get_rt_dates(self):
        dates = []
        for item in self.__rt_data:
            dates.append(item['datetime'])
        return dates

    def get_rt_highs(self):
        highs = []
        for item in self.__rt_data:
            highs.append(item['high'])
        return highs

    def get_rt_lows(self):
        lows = []
        for item in self.__rt_data:
            lows.append(item['low'])
        return lows

    def get_rt_opens(self):
        opens = []
        for item in self.__rt_data:
            opens.append(item['open'])
        return opens

    def get_rt_closes(self):
        closes = []
        for item in self.__rt_data:
            closes.append(item['close'])
        return closes

    def get_rt_volumes(self):
        volumes = []
        for item in self.__rt_data:
            volumes.append(item['volume'])
        return volumes

    def set_rt_period(self, per):
        self.__rt_period = per

    def get_quote_ask_price(self):
        return self.__quote['askPrice']

    def get_quote_candle_data(self):
        return self.__quote['tradeTimeInLong'], self.__quote['openPrice'], self.__quote['highPrice'],\
               self.__quote['lowPrice'], self.__quote['closePrice'], self.__quote['totalVolume']

    def get_quote_high(self):
        return self.__quote_high

    def get_quote_low(self):
        return self.__quote_low

    def get_quote_mark(self):
        return self.__quote['mark']

    def get_quote_volume(self):
        return self.__quote['totalVolume']

    def get_quote_datetime(self):
        return self.__quote['tradeTimeInLong']

    def get_dates_as_formatted(self, fmt='1', rt=False):
        to_ret = []

        if fmt == '1':
            for i in self.__rt_data[0]:
                to_ret.append(datetime.datetime.fromtimestamp(i / 1000.).strftime('%H:%M:%S\n%Y-%m-%d'))
        elif fmt == '2':
            for i in self.__dates:
                to_ret.append(datetime.datetime.fromtimestamp(i / 1000.).strftime('%Y-%m-%d'))
        elif fmt == '3':
            if rt:
                dates_in = self.get_rt_dates()
            else:
                dates_in = self.get_dates()
            dates = [mdates.epoch2num(i / 1000.) for i in dates_in]
            return dates

        else:
            to_ret = self.__dates
        return to_ret

    def get_candle_stick_data(self, fmt='1'):
        list = []
        for x in range(len(self.__open)):
            open = self.__open[x]
            close = self.__close[x]
            high = self.__high[x]
            low = self.__low[x]
            date = self.__dates[x] / 1000
            volume = self.__volume[x]
            temp = [date, open, high, low, close, volume]
            list.append(temp)

        if fmt == 'np':
            dates = [mdates.epoch2num(list[i][0]) for i in range(len(list))]
            for i in range(len(list)):
                list[i][0] = dates[i]

        return list

    def get_rt_candle_stick_data(self, fmt='1'):
        list = []
        for x in self.__rt_data:
            open = x['open']
            close = x['close']
            high = x['high']
            low = x['low']
            date = x['datetime'] / 1000
            volume = x['volume']
            temp = [date, open, high, low, close, volume]
            list.append(temp)

        if fmt == 'np':
            dates = [mdates.epoch2num(list[i][0]) for i in range(len(list))]
            for i in range(len(list)):
                list[i][0] = dates[i]

        return list

    def add_rt_data(self):
        start, end = start_end_date(2)
        data = api.get_price_history_2_api(start, end, 'minute', 1, 'true', self.__symbol)['candles']
        self.__rt_data = data

    def update_data(self, data):

        # Clearing member variables
        self.__dates = []
        self.__high = []
        self.__low = []
        self.__close = []
        self.__open = []
        self.__volume = []

        data_can = data['candles']
        try:
            for candle in data_can:
                self.__dates.append(candle['datetime'])
                self.__high.append(candle['high'])
                self.__low.append(candle['low'])
                self.__open.append(candle['open'])
                self.__close.append(candle['close'])
                self.__volume.append(candle['volume'])
        except IndexError:
            if data['empty'] == 'True':
                print('The data is empty but the message 200 came back')
            else:
                print(data['empty'])
        try:
            print('Last good data is: ', datetime.datetime.fromtimestamp(self.__dates[-1] / 1000.))
        except IndexError as e:
            print('No data was found from api request')
            print(data)

    def add_level_2_data(self):
        url = 'http://markets.cboe.com/us/equities/market_statistics/book/%s/' % self.get_symbol()
        # self.__web_page_driver = WebScraper(url)
        # From the beautiful soup object parse important data

    def update_quote_data(self):
        print('Updating quote data')
        data = api.get_quote_api(self.__symbol)['%s' % self.__symbol]

        for item in self.list_of_rt_vars:
            self.__quote[item] = data[item]

        if self.__quote_high == "":
            self.__quote_high = self.__quote['mark']
        elif self.__quote_high < self.__quote['mark']:
            self.__quote_high = self.__quote['mark']
        else:
            pass

        if self.__quote_low == "":
            self.__quote_low = self.__quote['mark']
        elif self.__quote_low > self.__quote['mark']:
            self.__quote_low = self.__quote['mark']
        else:
            pass




def start_end_date(per):
    import time
    offset = 0
    if datetime.datetime.today().weekday() == 0 and datetime.datetime.now().hour < 8:
        offset = 3
    if datetime.datetime.today().weekday() == 6:
        offset = 2

    t = int(int(time.time()) / 100) * 100 - 86400 * offset
    t_ms = t * 1000
    start = t - per * 86400
    start_ms = start * 1000
    return start_ms, t_ms

