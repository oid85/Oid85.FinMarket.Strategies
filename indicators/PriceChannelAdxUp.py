import backtrader as bt

from indicators.PriceHLCC import PriceHLCC


class PriceChannelAdxUp(bt.Indicator):
    lines = ('price_channel_adx_up',)
    params = (('period', 15),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.close = self.datas[0].close
        self.adx = bt.indicators.AverageDirectionalMovementIndex(self.datas[0], period=self.params.period)
        self.price_hlcc = PriceHLCC(self.datas[0], period=self.params.period)
        self.highest_hlcc = bt.indicators.Highest(self.price_hlcc, period=self.params.period)

    def next(self):
        pass
    