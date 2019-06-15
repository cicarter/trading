"""
From a list of important points with mins and maxs keyed:
    Find which line (ema, sma, linear) best correlates to the resistance and support lines
"""


def find_resistance(all_points, x_value):
    points = sorted([f for f in all_points if f[2] == 'min'])
    print('Points in stategy.py %s' % points)
    # Get the closest point given an x value
    current = ""
    past = ""

    for x in range(len(points)):
        if points[x][0] > x_value:
            current = x
            break
        past = x

    if current == "":
        main_point_index = points[-1]
    else:
        tester_curr = abs(points[current][0] - x_value)
        tester_past = abs(points[past][0] - x_value)
        if tester_curr <= tester_past:
            main_point_index = current
        else:
            main_point_index = past

    first = ""
    second = ""
    third = ""

    if main_point_index > 0:
        first = points[main_point_index]
        if main_point_index > 1:
            second = points[main_point_index - 1]
            if main_point_index > 2:
                third = points[main_point_index - 2]

    return first, second, third

class general():
    __maxs = []
    __mins = []

    def __init__(self, points):
        for point in points:
            if point[2] == 'max':
                self.__maxs.append(point)
            else:
                self.__mins.append(point)

        min_change = []
        max_change = []

        for x in range(len(self.__mins)):
            if x:
                min_change.append(self.get_slope(self.__mins[x - 1], self.__mins[x]))
            else:
                min_change.append('Null')

        for x in range(len(self.__maxs)):
            if x:
                max_change.append(self.get_slope(self.__maxs[x - 1], self.__maxs[x]))
            else:
                max_change.append('Null')

        self.__min_change = min_change
        self.__max_change = max_change


    @staticmethod
    def get_slope(point1, point2):
        return (point2[1] - point1[1]) / (point2[0] - point1[0])



# sym = 'AAPL'
# data_d = tdapi.get_price_history_api('day', '1', 'minute', '1', 'false', sym)['candles']
# pp = point_parser.PointParser(data_d)
#
# print(find_resistance(pp.print_significant(), 55))
