import backtrader as bt
import modules.data_module as dm
from TestStrategy import TestStrategy
from TestStrategy2 import TestStrategy2


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    df = dm.get_daily_candles_by_ticker('SBER', '2024-01-01', '2025-12-31')
    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1)
    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy, maperiod=15, logging=True)
    cerebro.addstrategy(TestStrategy2, maperiod=15, logging=True)
    cerebro.addsizer(bt.sizers.FixedSize,stake=10)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0)
    print('Starting Portfolio Value: {0:8.2f}'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('Final Portfolio Value: {0:8.2f}'.format(cerebro.broker.getvalue()))
    cerebro.plot()
