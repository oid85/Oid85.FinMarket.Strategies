import backtrader as bt


class PriceHLCC(bt.Indicator):
    lines = ('price_hlcc',)
    params = (('period', 15),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.close = self.datas[0].close

    def next(self):
        self.lines.highest_hlcc[0] = (self.high[0] + self.low[0] + self.close[0] + self.close[0]) / 4.0