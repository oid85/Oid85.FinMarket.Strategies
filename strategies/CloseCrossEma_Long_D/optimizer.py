import backtrader as bt
import modules.data_module as dm
import config
from strategies.CloseCrossEma_Long_D.CloseCrossEma_Long_D import CloseCrossEma_Long_D

if __name__ == '__main__':
    ticker = 'SBER'
    engine = bt.Cerebro()
    df = dm.get_daily_candles_by_ticker(ticker, config.daily_date_range['optimization_start_date'], config.daily_date_range['optimization_end_date'])
    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
    engine.adddata(data)
    engine.optstrategy(CloseCrossEma_Long_D, period=range(10, 55, 5), filter_period=range(70, 150, 5), logging=False)
    engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
    engine.broker.setcash(config.portfolio_money)
    engine.broker.setcommission(commission=0.0)
    engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    results = engine.run()
    dm.print_results(ticker, results)
