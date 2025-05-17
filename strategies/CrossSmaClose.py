import backtrader as bt


class CrossSmaClose(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('logging', False)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)

    def log(self, message, dt=None, logging=False):
        if self.params.logging or logging:
            dt = dt or self.datas[0].datetime.date(0)
            print('{0},TestStrategy,{1}'.format(dt.isoformat(), message))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {0:8.2f}, Size: {1:8.2f} Cost: {2:8.2f}, Comm: {3:8.2f}'.format(
                    order.executed.price, order.executed.size, order.executed.value,order.executed.comm))

            else:
                self.log('SELL EXECUTED, {0:8.2f}, Size: {1:8.2f} Cost: {2:8.2f}, Comm{3:8.2f}'.format(
                    order.executed.price, order.executed.size, order.executed.value, order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.order = self.buy()

        else:
            if self.dataclose[0] < self.sma[0]:
                self.order = self.sell()

    def stop(self):
        self.log('TestStrategy. MA Period: {0:8.2f} Ending Value: {1:8.2f}'.format(
            self.params.maperiod, self.broker.getvalue()), logging=True)