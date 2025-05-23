import backtrader as bt
import modules.data_module as dm
import config
from strategies.Supertrend_Long_D.Supertrend_Long_D import Supertrend_Long_D

if __name__ == '__main__':
    ticker = 'SBER'
    engine = bt.Cerebro()
    df = dm.get_daily_candles_by_ticker(ticker, config.start_date, config.end_date)
    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
    engine.adddata(data)
    engine.optstrategy(Supertrend_Long_D, period=range(10, 50, 5), multiplier=range(20, 30, 2), logging=False)
    engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
    engine.broker.setcash(config.portfolio_money)
    engine.broker.setcommission(commission=0.0)
    engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    results = engine.run()
    dm.print_results(ticker, results)
