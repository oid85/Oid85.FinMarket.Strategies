import backtrader as bt
import modules.data_module as dm
import config

from strategies.TestStrategy import TestStrategy

if __name__ == '__main__':
    for ticker in config.tickers:
        cerebro = bt.Cerebro()
        df = dm.get_daily_candles_by_ticker(ticker, config.start_date, config.end_date)
        data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy, maperiod=15, logging=False)
        cerebro.addsizer(bt.sizers.FixedSize,stake=1)
        cerebro.broker.setcash(1000000.0)
        cerebro.broker.setcommission(commission=0.0)
        print(ticker)
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        results = cerebro.run(maxcpus=1)
        sharpe = results[0].analyzers.sharpe.get_analysis()
        drawdown = results[0].analyzers.drawdown.get_analysis()
        trades = results[0].analyzers.trades.get_analysis()

        print(f'Sharpe Ratio: {sharpe["sharperatio"]}')
        print(f'Max Drawdown: {drawdown["max"]["drawdown"]}')
        print(f'Total Trades: {trades.total.total}')
        #cerebro.plot()
