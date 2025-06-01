import backtrader as bt
import modules.data_module as dm
import config

from indicators.PriceHLCC import PriceHLCC


class PriceChannelAdxUp(bt.Indicator):
    lines = ('price_channel_adx_up',)
    params = (('period', 15),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.close = self.datas[0].close
        self.adx = bt.indicators.AverageDirectionalMovementIndex(self.datas[0], period=self.params.period)
        self.price_hlcc = PriceHLCC(self.datas[0], period=self.params.period)
        self.highest_hlcc = bt.indicators.Highest(self.price_hlcc, period=self.params.period)

    def next(self):
        pass


class PriceChannelAdxUp_Simple(bt.Strategy):
    def __init__(self):
        self.close = self.datas[0].close
        self.order = None
        self.index = 0
        self.price_channel_adx_up = PriceChannelAdxUp(self.datas[0], period=self.params.period)


if __name__ == '__main__':
    ticker = 'SBER'
    engine = bt.Cerebro()
    df = dm.get_daily_candles_by_ticker(ticker, config.daily_date_range['backtest_start_date'], config.daily_date_range['backtest_end_date'])
    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
    engine.adddata(data)
    engine.addstrategy(PriceChannelAdxUp_Simple, period=15)
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