import backtrader as bt
import modules.data_module as dm
import config

from strategies.TestStrategy import TestStrategy

for ticker in config.tickers:
    if __name__ == '__main__':
        cerebro = bt.Cerebro()
        df = dm.get_daily_candles_by_ticker(ticker, config.start_date, config.end_date)
        data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
        cerebro.adddata(data)
        cerebro.optstrategy(TestStrategy, maperiod=range(10, 30, 5), logging=False)
        cerebro.addsizer(bt.sizers.FixedSize,stake=1)
        cerebro.broker.setcash(1000000.0)
        cerebro.broker.setcommission(commission=0.0)
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        results = cerebro.run(maxcpus=1)
        print(len(results))
