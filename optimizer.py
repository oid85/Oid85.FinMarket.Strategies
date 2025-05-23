import backtrader as bt
import modules.data_module as dm
import config

if __name__ == '__main__':
    dm.clear_optimization_result()
    tickerIndex = 0
    count = 0
    for ticker in config.tickers:
        tickerIndex += 1
        strategyIndex = 0
        for key in config.strategies.keys():
            strategyIndex += 1
            count += 1
            progresPercent = count / (len(config.tickers) * len(config.strategies)) * 100.0
            print(f'Оптимизация {progresPercent} %. Тикер {tickerIndex} из {len(config.tickers)}. Стратегия {strategyIndex} из {len(config.strategies)}')
            strategy = config.strategies[key]['strategy']
            params = config.strategies[key]['params']
            engine = bt.Cerebro()
            df = dm.get_daily_candles_by_ticker(ticker, config.start_date, config.end_date)
            data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
            engine.adddata(data)
            engine.optstrategy(strategy, **params)
            engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
            engine.broker.setcash(config.portfolio_money)
            engine.broker.setcommission(commission=0.0)
            engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
            engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
            engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
            results = engine.run()
            dm.save_optimization_results(ticker, strategy.settings, results)
