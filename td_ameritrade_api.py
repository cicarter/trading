import requests
import json
import token_handler

th = token_handler.TokenHandler()
th.save_token()
token = th.get_token()


def get_account_api(fields):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {'fields': fields}
    return requests.get('https://api.tdameritrade.com /v1/accounts/490601716', headers=headers, data=data).text


# Date needs to be in format yyyy-MM-dd
def get_hours_for_a_single_market_api(date, market):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {'apikey': 'CICARTER8080@AMER.OAUTHAP', 'date': date}
    return requests.get('https: // api.tdameritrade.com /v1/marketdata/%s/hours' % market,
                        data=data, headers=headers).text


def get_price_history_api(per_type, period, ft, feq, nehd, stock, print_url=False):
    # If delayed data needed -which should be never- pass the client_id

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    url = 'https://api.tdameritrade.com/v1/marketdata/%s/pricehistory?periodType=' \
          '%s&period=%s&frequencyType=%s&frequency=%s&needExtendedHoursData=%s' % \
          (stock, per_type, period, ft, feq, nehd)
    if print_url:
        print(url)

    test = json.loads(requests.get(url, headers=headers).text)
    try:
        if test['empty'] != 'True':
            return test
    except KeyError as e:
        raise ValueError('The api call failed to get response try running with print_url set to True')


def get_price_history_2_api(start_date, end_date, feq_type, feq, extended_hours, stock, print_url=False):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    url = 'https://api.tdameritrade.com/v1/marketdata/%s/pricehistory?frequencyType=' \
          '%s&frequency=%s&endDate=%s&startDate=%s&needExtendedHoursData=%s' % \
          (stock, feq_type, feq, end_date, start_date, extended_hours)
    if print_url:
        print(url)
    test = json.loads(requests.get(url, headers=headers).text)
    if test['empty'] == 'True':
        raise ValueError('The api call failed to get response try running with print_url set to True')

    else:
        return test

# Test to see says forbidden


def create_watch_list_api(json_watch_list):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {json_watch_list}
    return json.loads(requests.post('https://api.tdameritrade.com/v1/accounts/490601716/watchlists',
                                    headers=headers, data=data))


def get_watch_list_for_single_account_api():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {}
    return requests.get('https://api.tdameritrade.com/v1/accounts/490601716/watchlists',
                        headers=headers, data=data)


def create_saved_order_api(saved_order_data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {saved_order_data}
    return requests.post('https://api.tdameritrade.com/v1/accounts/cicarter98/savedorders',
                         data=data, headers=headers)


def delete_saved_order_api(saved_order_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {}
    return requests.delete('https://api.tdameritrade.com/v1/accounts/cicarter98/savedorders/{'
                           + saved_order_id + '}', data=data, headers=headers).text


def get_saved_order_api(saved_order_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {}
    return requests.get('https://api.tdameritrade.com/v1/accounts/cicarter98/savedorders/%s'
                        % saved_order_id, data=data, headers=headers).text


def get_saved_orders_by_path_api(saved_order_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {}
    return requests.get('https://api.tdameritrade.com/v1/accounts/cicarter98/%s' % saved_order_id,
                        data=data, headers=headers).text


def replace_saved_order_api(saved_order_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {saved_order_id}
    return requests.put('https://api.tdameritrade.com/v1/accounts/cicarter98/savedorders/%s' % saved_order_id,
                        data=data, headers=headers).text


def cancel_order_api(order_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {}
    return requests.delete('https://api.tdameritrade.com/v1/accounts/cicarter98/orders/' + order_id,
                           data=data, headers=headers)


def get_order_api(order_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = {}
    return requests.get('https://api.tdameritrade.com/v1/accounts/cicarter98/orders/' + order_id,
                        data=data, headers=headers)


def place_order(stock_json, account):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    data = stock_json
    return requests.post('https://api.tdameritrade.com/v1/accounts/%s/orders' % account, data=data, headers=headers)


def test_token_api(token2):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token2}
    data = {}
    return requests.get('https://api.tdameritrade.com/v1/accounts/490601716/preferences', headers=headers, data=data)


def get_15m_5d_graph(after_hours, stock):
    data = get_price_history_api('day', '5', 'minute', '15', after_hours, stock, token)
    return data


def get_ytd_graph(after_hours, stock):
    data = get_price_history_api('ytd', '1', 'weekly', '1', after_hours, stock, token)
    return data


def get_yesterday_and_todays_data_api():
    print('Trying to get yesterdays data')
    # Getting open, close, high, low from json data


def get_quote_api(stock):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    return json.loads(requests.get('https://api.tdameritrade.com/v1/marketdata/%s/quotes' % stock, headers=headers).text)
