import backtrader as bt
import modules.data_module as dm
import config

if __name__ == '__main__':
    strategies = dm.get_backtest_strategies()
    dm.clear_backtest_result()
    strategyIndex = 0
    for key in strategies.keys():
        strategyIndex = strategyIndex + 1
        progresPercent = strategyIndex / len(strategies) * 100.0
        print(f"Бэктест {progresPercent} %. Тикер {strategies[key]['ticker']}. Стратегия {strategyIndex} из {len(strategies)}")
        strategy = strategies[key]['strategy']
        params = strategies[key]['params']
        engine = bt.Cerebro()

        if strategy.settings['timeframe'] == 'D':
            df = dm.get_daily_candles_by_ticker(strategies[key]['ticker'], config.backtest_start_date, config.backtest_end_date)
        elif strategy.settings['timeframe'] == 'H':
            df = dm.get_daily_candles_by_ticker(strategies[key]['ticker'], config.backtest_start_date, config.backtest_end_date)
            
        data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
        engine.adddata(data)
        engine.addstrategy(strategy, **params)
        engine.addsizer(bt.sizers.PercentSizer, percents=config.percent_size)
        engine.broker.setcash(config.portfolio_money)
        engine.broker.setcommission(commission=0.0)
        engine.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        result = engine.run()
        dm.save_backtest_results(strategies[key]['ticker'], strategies[key]['strategy'].settings, [result])

dm.clear_strategy_signals()
dm.save_strategy_signals()
