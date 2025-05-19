import backtrader as bt
import modules.data_module as dm
import config

dm.clear_optimization_result()

if __name__ == '__main__':
    for ticker in config.tickers:
        for strategy, params in config.strategies.items():
            engine = bt.Cerebro()
            df = dm.get_daily_candles_by_ticker(ticker, config.start_date, config.end_date)
            data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
            engine.adddata(data)
            engine.optstrategy(strategy, **params)
            engine.addsizer(bt.sizers.PercentSizer, percents=50)
            engine.broker.setcash(config.cash)
            engine.broker.setcommission(commission=0.0)
            engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
            engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
            engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
            results = engine.run(maxcpus=1)
            dm.save_optimization_result(ticker, strategy.settings, results)
