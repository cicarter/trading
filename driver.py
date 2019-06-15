import td_ameritrade_api as tdapi
import charts
import stock
import point_parser
import indicators
import stategy

sym = 'AAPL'

s = stock.Stock(sym)
chart = charts.Charts(s)

data_d = tdapi.get_price_history_api('day', '1', 'minute', '1', 'false', sym)['candles']
print(data_d)
chart.plot_custom_plot(data_d, no_time=True)

pp = point_parser.PointParser(data_d)

y_coordinates = [pp.nine_window_ema[x] for x in pp.crossed]


closes = [f['close'] for f in data_d]

sma_120 = indicators.Indicators().simple_moving_average(closes, 120)
x_s = [i for i in range(len(sma_120))]

chart.plot_as_line(pp.xs, pp.nine_window_ema, 2)

x = [f[0] for f in pp.print_significant()]
y = [f[1] for f in pp.print_significant()]

print(pp.print_significant())
print(stategy.find_resistance(pp.print_significant(), 56))

rsi = indicators.Indicators().relative_strength(closes)
rsi_xs = [x for x in range(len(rsi))]
chart.plot_as_point(x, y, 2)
chart.plot_macd_histogram(3, data_d)
chart.plot_as_line(rsi_xs, rsi, 1)

chart.show()

