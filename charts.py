import matplotlib.ticker as mticker
from indicators import Indicators
from matplotlib.widgets import Button
import matplotlib.pyplot
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


class Charts:
    current_view = ""
    __stock = ""
    __axcut = ""
    __plot = ""

    axis_list = {}

    __bcut = ""

    def __init__(self, stock):
        self.__plot = matplotlib.pyplot
        self.__stock = stock
        self.add_plot()

    def plot_points(self, points, type_point='ro'):
        x_data = []
        y_data = []
        for p in points:
            x_data.append(p.x)
            y_data.append(p.y)

        self.axis_list[2].plot(x_data, y_data, type_point, linewidth=.4)

    def add_plot(self):
        self.__plot.suptitle(self.__stock.get_symbol())
        self.axis_list[2] = self.__plot.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1)
        self.axis_list[1] = self.__plot.subplot2grid((6, 1), (0, 0), rowspan=1, colspan=1, sharex=self.axis_list[2])
        self.axis_list[3] = self.__plot.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=self.axis_list[2])

    def clear_sub_plots(self):
        self.__plot.clf()
        self.add_plot()
        self.__axcut = self.__plot.axes([0.9, 0.0, 0.1, 0.075])
        self.__bcut = Button(self.__axcut, self.current_view, color='red', hovercolor='green')
        self.__bcut.on_clicked(self.change_view)


    def get_subplot(self, num):
        try:
            return self.axis_list[num]
        except KeyError as e:
            print(e)

    def on_click(self, event):
        if event.dblclick:
            print('Changing')
            self.change_view()

    def change_view(self, pos):
        self.clear_sub_plots()
        if self.current_view == "":
            self.make_graph_year(self.__stock)
        elif self.current_view == 'RT':
            self.make_graph_year(self.__stock)
        else:
            self.make_graph_rt(self.__stock)

    def make_graph_year(self, stock):
        self.current_view = 'Year'
        print('Current view year')
        i = Indicators()
        ema_slow, ema_fast, macd = i.moving_average_convergence(stock.get_closes(), nslow=26, nfast=12)
        sig_line = i.exp_moving_average(macd, 9)
        rsi = i.relative_strength(stock.get_closes())

        sma_window = 9
        ema_window = 9

        my_sma = i.simple_moving_average(stock.get_closes(), sma_window)
        my_ema = i.exp_moving_average(stock.get_closes(), ema_window)

        dates = stock.get_dates_as_formatted(fmt='3')
        for x in range(len(dates)):
            dates[x] = x
        # self.axis_list[3].plot(dates, macd)
        # self.axis_list[3].plot(dates, sig_line)
        # self.axis_list[3].plot(dates, macd - sig_line, 'k')
        # self.axis_list[3].axhline(y=0, color='b', linestyle='-')
        # self.axis_list[3].fill_between(dates, macd - sig_line, 0, alpha=.5, facecolor='#00ffe8', edgecolor='#00ffe8')
        # self.axis_list[3].spines['bottom'].set_color('#5998ff')
        # self.axis_list[3].spines['top'].set_color('#5998ff')
        # self.axis_list[3].spines['left'].set_color('#5998ff')
        # self.axis_list[3].spines['right'].set_color('#5998ff')

        ohlc = stock.get_candle_stick_data(fmt='np')
        for x in range(len(ohlc)):
            ohlc[x][0] = x
        candlestick_ohlc(self.axis_list[2], ohlc, colorup='green', colordown='red', width=.6)

        # self.axis_list[2].plot(dates[sma_window - 1:], my_sma, label='SMA')
        # self.axis_list[2].plot(dates, my_ema, label='EMA')
        self.axis_list[2].set_ylabel('Price')
        self.axis_list[2].legend(loc='upper right')
        self.__plot.suptitle(stock.get_symbol())

        # self.axis_list[1].plot(dates, rsi)
        # self.axis_list[1].xaxis.set_major_locator(mticker.MaxNLocator(10))
        # self.axis_list[1].get_xaxis().set_visible(False)
        # self.axis_list[2].get_xaxis().set_visible(False)

        self.axis_list[3].xaxis.set_major_locator(mticker.MaxNLocator(10))

        # md_dates = [datetime.datetime.strftime(mdates.num2date(i), '%Y-%m-%d') for i in dates]

        def my_date(x, pos):
            try:
                return md_dates[int(x)]
            except IndexError:
                return ''

        # self.axis_list[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        for lab in self.axis_list[3].xaxis.get_ticklabels():
            lab.set_rotation(30)

        return self.__plot

    def add_volume(self, fmt='1'):
        vol = self.__stock.get_volumes()

    def make_graph_rt(self, stock):
        self.current_view = 'RT'
        print('Current view real-time')

        i = Indicators()
        close = stock.get_rt_closes()

        ema_slow, ema_fast, macd = i.moving_average_convergence(close, nslow=26, nfast=12)
        sig_line = i.exp_moving_average(macd, 9)
        rsi = i.relative_strength(close)

        sma_window = 10
        ema_window = 10

        my_sma = i.simple_moving_average(close, sma_window)
        my_ema = i.exp_moving_average(close, ema_window)

        dates = stock.get_dates_as_formatted(fmt='3', rt=True)

        ohlc = stock.get_rt_candle_stick_data(fmt='np')

        for i in range(len(dates)):
            ohlc[i][0] = dates[i]

        for x in range(len(ohlc)):
            ohlc[x][0] = x

        print('OHLC RT is: %s' % ohlc)

        # self.axis_list[3].plot(dates, macd)
        # self.axis_list[3].plot(dates, sig_line)
        # self.axis_list[3].plot(dates, macd - sig_line, 'k')
        # self.axis_list[3].axhline(y=0, color='b', linestyle='-')
        # self.axis_list[3].fill_between(dates, macd - sig_line, 0, alpha=.5, facecolor='#00ffe8', edgecolor='#00ffe8')
        # self.axis_list[3].spines['bottom'].set_color('#5998ff')
        # self.axis_list[3].spines['top'].set_color('#5998ff')
        # self.axis_list[3].spines['left'].set_color('#5998ff')
        # self.axis_list[3].spines['right'].set_color('#5998ff')

        candlestick_ohlc(self.axis_list[2], ohlc, width=(.001 / 2), colorup='green', colordown='red')

        # self.axis_list[2].plot(dates[sma_window - 1:], my_sma, label='SMA')
        # self.axis_list[2].plot(dates, my_ema, label='EMA')
        self.axis_list[2].set_ylabel('Price')
        self.axis_list[2].legend(loc='upper right')
        self.__plot.suptitle(stock.get_symbol())

        # self.axis_list[1].plot(dates, rsi)
        # self.axis_list[1].xaxis.set_major_locator(mticker.MaxNLocator(10))
        # self.axis_list[1].get_xaxis().set_visible(False)
        # self.axis_list[2].get_xaxis().set_visible(False)
        #
        # self.axis_list[3].xaxis.set_major_locator(mticker.MaxNLocator(10))
        # self.axis_list[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        #
        # for lab in self.axis_list[3].xaxis.get_ticklabels():
        #     lab.set_rotation(30)

        return self.__plot

    def show(self):
        self.__plot.show()

    def hide(self):
        self.__plot.close()

    def add_data(self, lst_points, sub):

        for i in lst_points:
            if i.color == 'green':
                sub.plot(i.x, i.y, 'go')
            else:
                sub.plot(i.x, i.y, 'ro')

        sub.xaxis.set_major_locator(mticker.MaxNLocator(10))

    def plot_custom_plot(self, cs_data, no_time=False):
        self.clear_sub_plots()
        candle_list = []
        dates = [f['datetime'] / 1000.0 for f in cs_data]
        if not no_time:
            for candle in cs_data:
                candle_list.append([float(mdates.epoch2num(candle['datetime']/ 1000.0)),
                                    float(candle['open']),
                                    float(candle['high']),
                                    float(candle['low']),
                                    float(candle['close']),
                                    float(candle['volume'])])
        else:
            for x in range(len(cs_data)):
                candle_list.append([x,
                                    float(cs_data[x]['open']),
                                    float(cs_data[x]['high']),
                                    float(cs_data[x]['low']),
                                    float(cs_data[x]['close']),
                                    float(cs_data[x]['volume'])])

        # Changing the labels for the x-axis
        # self.axis_list[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # dates_formatted = [mdates.epoch2num(candle['datetime'] / 1000.) for candle in cs_data['candles']]
        # print('Dates formatted %s' % dates_formatted)

        self.axis_list[1].get_xaxis().set_visible(False)
        self.axis_list[2].get_xaxis().set_visible(False)

        candlestick_ohlc(self.axis_list[2], candle_list, colorup='green', colordown='red', width=.001)

    def create_default_chart(self, view='year'):
        self.axis_list[2] = self.__plot.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1)
        self.axis_list[1] = self.__plot.subplot2grid((6, 1), (0, 0), rowspan=1, colspan=1, sharex=self.axis_list[2])
        self.axis_list[3] = self.__plot.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=self.axis_list[2])

        self.__axcut = self.__plot.axes([0.9, 0.0, 0.1, 0.075])
        self.__bcut = Button(self.__axcut, self.current_view, color='red', hovercolor='green')
        self.__bcut.on_clicked(self.change_view)

        if view == 'rt':
            self.make_graph_rt(self.__stock)
            self.current_view = 'RT'
        else:
            self.make_graph_year(self.__stock)
            self.current_view = 'Year'

    def plot_as_point(self, data_x, data_y, axis, color='ro'):
        self.axis_list[axis].plot(data_x, data_y, color)

    def plot_as_line(self, data_x, data_y, axis):
        self.axis_list[axis].plot(data_x, data_y)

    def plot_macd_histogram(self, plot, macd_data, dates=None):
        close = [f['close'] for f in macd_data]
        xs = [x for x in range(len(close))]

        i = Indicators()
        ema_slow, ema_fast, macd = i.moving_average_convergence(close, nslow=26, nfast=12)
        sig_line = i.exp_moving_average(macd, 9)

        if dates:
            self.axis_list[plot].plot(dates, macd)
            self.axis_list[plot].plot(dates, sig_line)
            self.axis_list[plot].plot(dates, macd - sig_line, 'k')
            self.axis_list[plot].axhline(y=0, color='b', linestyle='-')
            self.axis_list[plot].fill_between(dates, macd - sig_line, 0, alpha=.5, facecolor='#00ffe8', edgecolor='#00ffe8')
            self.axis_list[plot].spines['bottom'].set_color('#5998ff')
            self.axis_list[plot].spines['top'].set_color('#5998ff')
            self.axis_list[plot].spines['left'].set_color('#5998ff')
            self.axis_list[plot].spines['right'].set_color('#5998ff')
        else:
            # self.axis_list[plot].plot(macd)
            # self.axis_list[plot].plot(sig_line)
            self.axis_list[plot].plot(macd - sig_line, color='k')
            self.axis_list[plot].axhline(y=0, color='b', linestyle='-')
            self.axis_list[plot].fill_between(xs, macd - sig_line, 0, alpha=.5, facecolor='#00ffe8', edgecolor='#00ffe8')
            self.axis_list[plot].spines['bottom'].set_color('#5998ff')
            self.axis_list[plot].spines['top'].set_color('#5998ff')
            self.axis_list[plot].spines['left'].set_color('#5998ff')
            self.axis_list[plot].spines['right'].set_color('#5998ff')

    def plot_histogram(self, data, plot):
        self.axis_list[plot].hist(data, bins=20)