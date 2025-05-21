import backtrader as bt


class Supertrend_Long_D(bt.Strategy):
    settings = {
        'id': '1031b21c-1439-4a9c-aea3-f389039d157b',
        'version': 1,
        'timeframe': 'D'
    }

    params = (
        ('period', 15),
        ('multiplier', 2.5),
        ('logging', False)
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.order = None
        self.highest = bt.indicators.Highest(self.datas[0], period=self.params.period)
        self.lowest = bt.indicators.Lowest(self.datas[0], period=self.params.period)
        self.atr = bt.indicators.AverageTrueRange(self.datas[0], period=self.params.period)

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
        if self.order:
            return

        up = (self.highest[0] + self.lowest[0]) / 2.0 + self.atr[0] * self.params.multiplier
        down = (self.highest[0] + self.lowest[0]) / 2.0 - self.atr[0] * self.params.multiplier

        signal_open_long = self.close[0] > down
        signal_open_long = self.close[0] < down

        if not self.position:
            if signal_open_long:
                self.order = self.buy()

        else:
            if signal_open_long:
                self.order = self.sell()
