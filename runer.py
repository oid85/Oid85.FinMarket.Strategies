import backtrader as bt
import modules.data_module as dm
import config

if __name__ == '__main__':
    strategies = dm.get_backtest_strategies()
    dm.clear_backtest_result()
    strategyIndex = 0
    for id, strategy_data in strategies.items():
        strategyIndex = strategyIndex + 1
        progresPercent = strategyIndex / len(strategies) * 100.0
        print(f"Бэктест {progresPercent} %. Тикер {strategy_data['ticker']}. Стратегия {strategyIndex} из {len(strategies)}")
        engine = bt.Cerebro()
        df = dm.get_daily_candles_by_ticker(strategy_data['ticker'], config.start_date, config.end_date)
        data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
        engine.adddata(data)
        engine.addstrategy(strategy_data['strategy'], **strategy_data['params'])
        engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
        engine.broker.setcash(config.strategy_money)
        engine.broker.setcommission(commission=0.0)
        engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        result = engine.run()
        dm.save_backtest_results(strategy_data['ticker'], strategy_data['strategy'].settings, [result])

dm.clear_strategy_signals()
dm.save_strategy_signals()
