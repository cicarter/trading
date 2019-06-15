class Pattern:
    __points = []
    __runner_points = []


    def __init__(self, points):
        self.__points = points

    @staticmethod
    def id_run_direction():
        print('Finish')
        # Look for change in direction for significant points

    def id_horizontal_resistance(self, buffer=.05):
        for point in self.__runner_points:
            if point[1] == 'max':
                return point

    def id_horizontal_support(self, buffer=.05):
        for point in self.__runner_points:
            if point[1] == 'min':
                return point



