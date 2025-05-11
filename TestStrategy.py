import backtrader as bt


class TestStrategy(bt.Strategy):
    config = {
        'Name': 'TestStrategy',
        'Key': '0e3d2fee-3eaa-4e87-8ae2-e09a94d04c6b',
        'TimeFrame': 'D',
        'Enable': False
    }

    params = (
        ('Period', 26),
        ('EnableLog ', False)
    )

    def log(self, txt, dt=None, enable_log=False):
        if self.p.EnableLog or enable_log:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.ClosePrices = self.datas[0].close
        self.Order = None
        self.Sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.SMAPeriod)
        self.StartMoney = self.broker.getValue()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'Bought @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'Sold @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order {order.status}')
        self.Order = None

    def notify_trade(self, trade):
        if not trade.isclosed: # позиция не закрыта
            return
        self.log(f'Trade PnL = {trade.pnl:.2f}, Net = {trade.pnlcomm:.2f}')

    def next(self):
        self.log(f'Close={self.ClosePrices[0]:.2f}')
        if self.Order: # есть неисполненная заявка
            return

        if not self.position: # позиции нет
            signal_buy = self.ClosePrices[0] > self.Sma[0]
            if signal_buy:
                self.log('Buy')
                self.Order = self.buy()

        else: # позиция есть
            signal_sell = self.ClosePrices[0] < self.Sma[0]
            if signal_sell:
                self.log('Sell')
                self.Order = self.sell()

    def stop(self):
        self.log(f'Money = {(self.broker.getValue() - self.StartMoney):.2f}', enable_log=True)
