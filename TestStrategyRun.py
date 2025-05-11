import backtrader as bt
from TestStrategy import TestStrategy

cerebro = bt.Cerebro()
cerebro.optstrategy(TestStrategy, Period=range(10, 50))
data = bt.feeds.PostgresData('SBER', '2025-01-01', '2025-12-31')
cerebro.adddata(data)
cerebro.broker.setcash(1000000)
cerebro.addsizer(bt.sizers.SizerFix, stake=10)
cerebro.broker.setcommission(commission=0.001)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
results = cerebro.run()
stats = {}
for result in results:
    p = result[0].p.Period
    analysis = result[0].analyzers.TradeAnalyzer.get_analysis()
    v = analysis['pnl']['net']['total']
    stats[p] = v
    print(f'SMA({p}), {v:.2f}')
max_stat = max(stats.items(), key=lambda x: x[1])
min_stat = min(stats.items(), key=lambda x: x[1])
print(f'Max stat: SMA({max_stat[0]}), {max_stat[1]:.2f}')
print(f'Min stat: SMA({min_stat[0]}), {min_stat[1]:.2f}')
