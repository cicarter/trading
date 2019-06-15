import math

def is_in_hours(dates):
    for date in dates:
        print(type(date))

def round_to_ten(x):
    if int(str(int(x))[-1:]) >= 5:
        return int(str(int(str(int(x))[-2:-1]) + 1) + '0')
    else:
        return int(str(int(str(int(x))[-2:-1])) + '0')
    # return int(math.ceil(x / 10.0)) * 10

one_day_in_datetime_ms = 86400000

