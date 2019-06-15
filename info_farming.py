import td_ameritrade_api as tdi
import csv
import json
from os.path import isfile
import pickle
import calendar, time
import datetime

MAIN_DIR = '/media/root/Catch All/stocks/td_ameritrading'
CVS_DIR = '/root/Downloads/company_list.csv'

# Getting a list of stocks
f = open('/root/Downloads/company_list.csv', 'r')
reader = csv.DictReader(f, fieldnames=("Symbol", "Name", "LastSale",
                                       "MarketCap", "IPOyear", "Sector", "industry", "Summary Quote"))

out = json.dumps([row for row in reader])
data = json.loads(out)
syms = [stock["Symbol"] for stock in data]
syms = syms[1:]


def get_data_with_period(stock_name, period, p_length):
    PER_TYPE = period
    PERIOD = p_length
    FT = 'daily'
    FEQ = '1'
    NEDH = 'true'
    print_url = False
    to_ret = tdi.get_price_history_api(PER_TYPE, PERIOD, FT, FEQ, NEDH, stock_name, print_url=print_url)
    return to_ret


def get_timed_data(stock_name, start, end, feq_type='minute'):
    FEQ_TYPE = feq_type
    FEQ = '1'
    EXTENED_HOUR = True
    PRINT_URL = False
    return tdi.get_price_history_2_api(start, end, FEQ_TYPE, FEQ, EXTENED_HOUR, stock_name, print_url=PRINT_URL)


def save_stock_to_file(stock_as_dict, date, dir='DEFALUT'):
    try:
        if dir == 'DEFAULT':
            with open('%s/%s.pkl' % ('%s/day_data' % MAIN_DIR, stock_as_dict['symbol']), 'wb') as out_file:
                stock_as_dict['first_date'] = date
                pickle.dump(stock_as_dict, out_file, pickle.HIGHEST_PROTOCOL)
        else:
            with open('%s/%s.pkl' % (dir, stock_as_dict['symbol']), 'wb') as out_file:
                stock_as_dict['first_date'] = date
                pickle.dump(stock_as_dict, out_file, pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(e)
        pass


def load_stock_from_file(filename):
    with open(filename, 'rb') as in_file:
        return pickle.load(in_file)


def create_base_info(sym):
    # Getting the data for a 1 d 1 minute graph
    try:
        cs_data = get_data_with_period(sym, 'year', '5')

        # Getting the datetime from first candlestick
        date = cs_data['candles'][0]['datetime']
        save_stock_to_file(cs_data,  date)

    except Exception as e:
        print(e)
        pass


def create_3_week_minute_data(sym):
    try:
        # Get today's datetime in milliseconds since epoch
        today_datetime = calendar.timegm(time.strptime('%s 00:00:00' % datetime.datetime.now().date(), '%Y-%m-%d %H:%M:%S')) * 1000
        # Subtract 3 weeks from datetime number
        start_date = today_datetime - (86400000 * 21)
        to_save = get_timed_data(sym, start_date, today_datetime)
        save_stock_to_file(to_save, start_date, dir='%s/minute_data' % MAIN_DIR)

    except Exception as e:
        print(e)


def add_more_data_to_stock(sym):
    # Loading the minute data
    try:
        stock_obj = load_stock_from_file('%s/minute_data/%s.pkl' % (MAIN_DIR, sym))
        last_time = stock_obj['candles'][-1]['datetime']
        today_time = int(time.time()) * 1000
        to_append = get_timed_data(sym, last_time, today_time)
        print(len(stock_obj['candles']))
        for candle in to_append['candles']:
            if candle['datetime'] > stock_obj['candles'][-1]['datetime']:
                stock_obj['candles'].append(candle)
        save_stock_to_file(stock_obj, stock_obj['first_date'], '%s/minute_data' % MAIN_DIR)

    except Exception as e:
        print('Exception %s' % e)


for sym in syms:
    add_more_data_to_stock(sym)
    time.sleep(1)