import backtrader as bt
import modules.data_module as dm
import config


class PriceHLCC(bt.Indicator):
    lines = ('price_hlcc',)
    params = ()

    def __init__(self):
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.close = self.datas[0].close

    def next(self):
        self.lines.highest_hlcc[0] = (self.high[0] + self.low[0] + self.close[0] + self.close[0]) / 4.0

class PriceHLCC_Simple(bt.Strategy):
    def __init__(self):
        self.close = self.datas[0].close
        self.order = None
        self.index = 0
        self.price_hlcc = PriceHLCC(self.datas[0])

if __name__ == '__main__':
    ticker = 'SBER'
    engine = bt.Cerebro()
    df = dm.get_daily_candles_by_ticker(ticker, config.daily_date_range['backtest_start_date'], config.daily_date_range['backtest_end_date'])
    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
    engine.adddata(data)
    engine.addstrategy(PriceHLCC_Simple)
    engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
    engine.broker.setcash(config.portfolio_money)
    engine.broker.setcommission(commission=0.0)
    engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    engine.addanalyzer(bt.analyzers.Returns, _name='returns')
    result = engine.run()
    dm.print_results(ticker, [result])
    engine.plot()