import backtrader as bt

import config


class Supertrend_Long_D(bt.Strategy):
    settings = {
        'id': '1031b21c-1439-4a9c-aea3-f389039d157b',
        'description': 'Супертренд',
        'version': 1,
        'timeframe': 'D'
    }

    params = (
        ('period', 15),
        ('multiplier', 25),
        ('logging', False)
    )

    def __init__(self):
        self.multiplier = self.params.period / 10.0
        self.close = self.datas[0].close
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.order = None
        self.index = 0
        self.highest = bt.indicators.Highest(self.datas[0], period=self.params.period)
        self.lowest = bt.indicators.Lowest(self.datas[0], period=self.params.period)
        self.atr = bt.indicators.AverageTrueRange(self.datas[0], period=self.params.period)
        self.is_bullish = None
        self.upper_band = None
        self.lower_band = None
        self.UpperBand = None
        self.LowerBand = None
        self.SuperTrend = None

    def log(self, message, dt=None, logging=False):
        if self.params.logging or logging:
            dt = dt or self.datas[0].datetime.date(0)
            print('{0}, {1}'.format(dt.isoformat(), message))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'LONG PRICE={order.executed.price} SIZE={order.executed.size} COST={order.executed.value}')

            else:
                self.log(f'SHORT PRICE={order.executed.price} SIZE={order.executed.size} COST={order.executed.value}')

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.index += 1

        if self.order:
            return

        if self.index >= config.stabilization_period_in_candles:
            mid = (self.highest[0] + self.lowest[0]) / 2.0
            atr = self.atr[0]
            prev_close = self.close[-1]

            upper_eval = mid + (self.multiplier * atr)
            lower_eval = mid - (self.multiplier * atr)

            if self.index == config.stabilization_period_in_candles:
                self.is_bullish = self.close[0] >= mid
                self.upper_band = upper_eval
                self.lower_band = lower_eval

            if upper_eval < self.upper_band or prev_close > self.upper_band:
                self.upper_band = upper_eval

            if lower_eval > self.lower_band or prev_close < self.lower_band:
                self.lower_band = lower_eval

            if self.close[0] <= self.lower_band if self.is_bullish else self.upper_band:
                self.SuperTrend = self.upper_band
                self.UpperBand = self.upper_band
                self.is_bullish = False

            else:
                self.SuperTrend = self.lower_band
                self.LowerBand = self.lower_band
                self.is_bullish = True

            signal_open_long = self.close[0] > self.SuperTrend
            signal_close_long = self.close[0] < self.SuperTrend

            if not self.position:
                if signal_open_long:
                    self.order = self.buy()

            else:
                if signal_close_long:
                    self.order = self.sell()
