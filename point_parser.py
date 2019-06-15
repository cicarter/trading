"""
From some candle stick data, this will create a list of points and determine how much of one pattern is embedded in
the data.
"""
import indicators
import statistics


class PointParser:
    nine_window_ema = []
    local_extrema_x_values = []
    data = []
    xs = []
    ys = []
    derivatives = []
    crossed = []
    as_points = []
    __points_importance = []
    __significant_points = []
    __POINT_THRESHOLD = ''
    __delta_y_list = ''

    # Create a 9 window ema
    def __init__(self, data_in, data_type='cs'):
        self.data = data_in
        if data_type == 'cs':
            dict = {}
            # convert candlestick data into x and y coordinates
            # OPTIMIZE this for loop should not exist stock should be in best format
            # to make point parser work
            for x in range(len(data_in)):
                dict[x] = data_in[x]['close'] # candle[4] is datetime in seconds*
            lists = dict.items()
            xs, ys = zip(*lists)
            self.nine_window_ema = indicators.Indicators.exp_moving_average(ys, 9)
            self.xs = xs
            self.ys = ys

        else:
            try:
                self.nine_window_ema = indicators.Indicators.exp_moving_average(data_in, 9)
            except Exception as e:
                print(e)

        der = self.calculate_derivative(self.xs, self.nine_window_ema)
        smooth_der = indicators.Indicators.exp_moving_average(der, 1) # Change 1 as needed
        self.derivatives = smooth_der
        self.crossed = self.crossed_zero(smooth_der)
        self.add_points()
        for _ in self.as_points:
            self.__points_importance.append(100)
        self.__important_points_creator()
        self.__POINT_THRESHOLD = 90

    @staticmethod
    def calculate_derivative(xs, ys):
        dy_dx = []
        if len(xs) != len(ys):
            raise ValueError('parameter 1 and parameter 2 are not the same length')
        else:
            for itt in range(len(xs)):
                if itt == 0:
                    pass
                else:
                    try:
                        der = float((ys[itt] - ys[itt - 1]) / (xs[itt] - xs[itt - 1]))
                        dy_dx.append(der)
                    except ZeroDivisionError:
                        pass

        return dy_dx

    @staticmethod
    def crossed_zero(data_in):
        crossed_zero_at_list = []
        above = False
        if data_in[0] >= 0:
            above = True

        for x in range(len(data_in)):
            if data_in[x] > 0 and not above:
                crossed_zero_at_list.append(x)
                above = True
            elif data_in[x] < 0 and above:
                crossed_zero_at_list.append(x)
                above = False
            elif data_in[x] == 0:
                crossed_zero_at_list.append(x)
        return crossed_zero_at_list

    def add_point_significant(self):
        to_ret = []
        for x in range(len(self.__points_importance)):
            if self.__points_importance[x] > self.__POINT_THRESHOLD:
                to_ret.append(self.as_points[x])
        self.__significant_points = to_ret

    def print_significant(self):
        return self.__significant_points


    def add_points(self):
        for point in self.crossed:
            val = ''
            if self.nine_window_ema[point - 1] > self.nine_window_ema[point]:
                val = 'min'
            else:
                val = 'max'
            self.as_points.append([point, self.nine_window_ema[point], val])


    def __important_points_creator_1(self):
        THRESHOLD = 0.5
        total_distance = 0.0
        delta_y_list = [] # Change var name to something distance related

        # From left to right
        for x in range(len(self.as_points)):
            if x:
                delta_y = self.as_points[x][1] - self.as_points[x - 1][1]
                delta_x = self.as_points[x][0] - self.as_points[x - 1][0]
                distance = (delta_x**2. + delta_y**2) ** (1/2.)
                total_distance += delta_y
                delta_y_list.append(delta_y)

        total = 0
        to_ret = []
        for x in delta_y_list:
            total += x

        avg_delta_y = float(total / len(delta_y_list))

        stdev = statistics.stdev(delta_y_list)
        i = 0
        for x in range(len(delta_y_list)):
            if delta_y_list[x] > avg_delta_y + THRESHOLD * stdev or delta_y_list[x] < avg_delta_y - THRESHOLD * stdev:
                to_app = [self.as_points[x][0], self.as_points[x][1]]
                to_ret.append(to_app)
                try:
                    if delta_y_list[x] > avg_delta_y:
                        to_app = [self.as_points[x + 1][0], self.as_points[x + 1][1]]
                        to_ret.append(to_app)
                except KeyError:
                    pass
                i += 1

        self.__significant_points = to_ret

    def __important_points_creator_2p0(self):
        important_points = []
        total_x_var = 0
        for x in range(len(self.as_points)):
            if x:
                to_add = self.as_points[x][0] - self.as_points[x - 1][0]
                total_x_var += to_add
                print(to_add)

        avg_x_dist = total_x_var / len(self.as_points)

        # Getting rid of clumps of data:
        for x in range(len(self.as_points)):
            if x:
                if not self.as_points[x][0] - self.as_points[x - 1][0] < avg_x_dist * .75:
                    important_points.append(self.as_points[x])
            else:
                important_points.append(self.as_points[x])

        self.__significant_points = important_points
        print(important_points)

    def __important_points_creator_trash(self):
        direction = ''
        important_points = []
        for x in range(len(self.as_points)):
            if x:
                if self.as_points[x][1] > self.as_points[x - 1][1] and direction == 'down':
                    direction = 'up'
                    important_points.append(self.as_points[x])
                elif self.as_points[x][1] < self.as_points[x - 1][1] and direction == 'up':
                    direction = 'down'
                    important_points.append(self.as_points[x])
                elif self.as_points[x][1] > self.as_points[x - 1][1]:
                    direction = 'up'
                else:
                    direction = 'down'

        self.__significant_points = important_points

    def __important_points_creator(self):
        all_points = self.as_points
        important_ltr = []
        total_x = 0
        total_y = 0
        length = 0

        for x in range(len(all_points)):
            if x:
                total_x += abs(all_points[x][0] - all_points[x - 1][0])
                total_y += abs(all_points[x][1] - all_points[x - 1][1])
                length += 1

        y_thresh = total_y / length
        x_thresh = total_x / length
        middle = -1

        # Left to right
        for x in range(len(all_points)):
            if x == 0:
                important_ltr.append(all_points[x])
            elif middle > x:
                if middle == x:
                    important_ltr.append(all_points[middle])
            # elif abs(all_points[x-1][0] - all_points[x][0]) > x_thresh:
            elif abs(all_points[x-1][1] - all_points[x][1]) > y_thresh:
                important_ltr.append(all_points[x])
                important_ltr.append(all_points[x - 1])
            else:
                start = x
                temp = x

                while abs(all_points[temp - 1][0] - all_points[temp][0]) < x_thresh:
                    if temp < len(all_points) - 1:
                        temp += 1
                    else:
                        break

                middle = int((start + temp) / 2)

        print('X_Thresh %s' % x_thresh)
        important_ltr = sorted(important_ltr)
        for x in range(len(important_ltr)):
            if important_ltr[x] == important_ltr[x - 1]:
                important_ltr[x] = 'null'

        for point in important_ltr:
            if point == 'null':
                important_ltr.remove(point)

        self.__significant_points = important_ltr
