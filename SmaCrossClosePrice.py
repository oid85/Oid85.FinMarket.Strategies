from datetime import datetime
import backtrader as bt
import modules.data_loader as dl


class SmaCrossClosePrice(bt.Strategy):
    config = {
        'Name': 'SmaCrossClosePrice',
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


cerebro = bt.Cerebro()
cerebro.optstrategy(SmaCrossClosePrice, Period=range(10, 50))
data = dl.get_daily_candles_by_ticker('SBER', '2020-01-01', '2025-12-31')
cerebro.adddata(data)
cerebro.broker.setcash(1000000)
cerebro.addsizer(bt.sizers.SizerFix, stake=10)
cerebro.broker.setcommission(commission=0.001)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
results = cerebro.run()
stats = {}
for result in results:
    p = result[0].p.Period
    analysis = result[0].analyzers.TradeAnalyzer.get_analysis()
    v = analysis['pnl']['net']['total']
    stats[p] = v
    print(f'SMA({p}), {v:.2f}')
max_stat = max(stats.items(), key=lambda x: x[1])
min_stat = min(stats.items(), key=lambda x: x[1])
print(f'Max stat: SMA({max_stat[0]}), {max_stat[1]:.2f}')
print(f'Min stat: SMA({min_stat[0]}), {min_stat[1]:.2f}')
