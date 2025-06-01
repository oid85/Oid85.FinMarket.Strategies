import backtrader as bt
import config


class CloseCrossEma_Long_D(bt.Strategy):
    settings = {
        'id': '208e13f2-7609-4d5c-832e-71fa75319c22',
        'description': 'Цена закрытия выше EMA. Фильтр EMA',
        'version': 1,
        'timeframe': 'D'
    }

    params = (
        ('period', 15),
        ('filter_period', 70),
        ('logging', False)
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.order = None
        self.index = 0
        self.ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.period)
        self.filter_ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.filter_period)

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
            signal_open_long = self.close[0] > self.ema[0] and self.close[0] > self.filter_ema[0]
            signal_close_long = self.close[0] < self.ema[0] or self.close[0] < self.filter_ema[0]

            if not self.position:
                if signal_open_long:
                    self.order = self.buy()

            else:
                if signal_close_long:
                    self.order = self.sell()
