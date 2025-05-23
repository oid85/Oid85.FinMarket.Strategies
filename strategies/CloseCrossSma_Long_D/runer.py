import backtrader as bt
import modules.data_module as dm
import config
from strategies.CloseCrossSma_Long_D.CloseCrossSma_Long_D import CloseCrossSma_Long_D

if __name__ == '__main__':
    ticker = 'SBER'
    engine = bt.Cerebro()
    df = dm.get_daily_candles_by_ticker(ticker, config.backtest_start_date, config.backtest_end_date)
    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
    engine.adddata(data)
    engine.addstrategy(CloseCrossSma_Long_D, period=15, logging=True)
    engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
    engine.broker.setcash(config.portfolio_money)
    engine.broker.setcommission(commission=0.0)
    engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    result = engine.run()
    dm.print_results(ticker, [result])
    engine.plot()

