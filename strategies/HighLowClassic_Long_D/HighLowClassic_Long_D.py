import backtrader as bt


class HighLowClassic_Long_D(bt.Strategy):
    settings = {
        'id': '5c188831-8cea-43f6-b3d1-9ced5505ce8d',
        'description': 'Пробой Highest, выход по Lowest',
        'version': 1,
        'timeframe': 'D'
    }

    params = (
        ('period', 15),
        ('logging', False)
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.order = None
        self.index = 0
        self.highest = bt.indicators.Highest(self.datas[0], period=self.params.period)
        self.lowest = bt.indicators.Lowest(self.datas[0], period=self.params.period)

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

        if self.index >= self.params.period:
            signal_open_long = self.close[0] > self.highest[-1]
            signal_close_long = self.close[0] < self.lowest[0]

            if not self.position:
                if signal_open_long:
                    self.order = self.buy()

            else:
                if signal_close_long:
                    self.order = self.sell()
