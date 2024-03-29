import numpy as np

class Indicators:

    # Classical Indicators
    @staticmethod
    def exp_moving_average(values, window):
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()
        a = np.convolve(values, weights, mode='full')[:len(values)]
        a[:window] = a[window]
        return a

    @staticmethod
    def simple_moving_average(x, n):
        weights = np.repeat(1.0, n) / n
        smas = np.convolve(x, weights, 'valid')
        return smas

    @staticmethod
    def relative_strength(prices, n=14):
        deltas = np.diff(prices)
        seed = deltas[:n + 1]
        up = seed[seed >= 0].sum() / n
        down = -seed[seed < 0].sum() / n
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100. / (1. + rs)

        for i in range(n, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter

            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (n - 1) + upval) / n
            down = (down * (n - 1) + downval) / n

            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)

        return rsi

    def moving_average_convergence(self, x, nslow=26, nfast=12):
        """
        compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
        return value is emaslow, emafast, macd which are len(x) arrays
        """
        emaslow = self.exp_moving_average(x, nslow)
        emafast = self.exp_moving_average(x, nfast)

        return emaslow, emafast, emafast - emaslow

    # Custom Indicators

    # High relative volume