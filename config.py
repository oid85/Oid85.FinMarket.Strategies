import datetime
from datetime import timedelta

from strategies.CloseCrossEma_Long_D.CloseCrossEma_Long_D import CloseCrossEma_Long_D
from strategies.HmaInclination_Long_D.HmaInclination_Long_D import HmaInclination_Long_D
from strategies.Supertrend_Long_D.Supertrend_Long_D import Supertrend_Long_D
from strategies.HighLowClassic_Long_D.HighLowClassic_Long_D import HighLowClassic_Long_D
from strategies.HighLowMiddle_Long_D.HighLowMiddle_Long_D import HighLowMiddle_Long_D

host = '26.147.25.39'
port = 5432
database = 'finmarket_prod'
user = 'postgres'
password = 'postgres'

stabilization_period_in_candles = 100
optimization_window_in_days = 3 * 365
backtest_window_in_days = 180
daily_stabilization_period_in_days = 150
hourly_stabilization_period_in_days = 15
today = datetime.datetime.today()

daily_date_range = {
    'optimization_start_date': (today - timedelta(days=backtest_window_in_days) - timedelta(days=optimization_window_in_days) - timedelta(days=daily_stabilization_period_in_days)).date(),
    'optimization_end_date': (today - timedelta(days=backtest_window_in_days)).date(),
    'backtest_start_date': (today - timedelta(days=backtest_window_in_days) - timedelta(days=daily_stabilization_period_in_days)).date(),
    'backtest_end_date': today.date()
}

hourly_date_range = {
    'optimization_start_date': (today - timedelta(days=backtest_window_in_days) - timedelta(days=optimization_window_in_days) - timedelta(days=hourly_stabilization_period_in_days)).date(),
    'optimization_end_date': (today - timedelta(days=backtest_window_in_days)).date(),
    'backtest_start_date': (today - timedelta(days=backtest_window_in_days) - timedelta(days=hourly_stabilization_period_in_days)).date(),
    'backtest_end_date': today.date()
}

portfolio_money = 1000000.0
percent_size = 50

optimization_result_filter = {
    'profit_factor': 3.0,
    'recovery_factor': 3.0,
    'max_drawdown_percent': 20.0,
}

backtest_result_filter = {
    'profit_factor': 0.0,
    'recovery_factor': 0.0,
    'max_drawdown_percent': 20.0,
}

strategies = {
    '208e13f2-7609-4d5c-832e-71fa75319c22': {
        'strategy': CloseCrossEma_Long_D,
        'params': {'period': range(10, 55, 5), 'filter_period': range(70, 150, 5), 'logging': False}
    },

    '41b8cba8-8d1b-4a42-867b-03e798d888ad': {
        'strategy': HmaInclination_Long_D,
        'params': {'period': range(10, 55, 5), 'logging': False}
    },

    '1031b21c-1439-4a9c-aea3-f389039d157b': {
        'strategy': Supertrend_Long_D,
        'params': {'period': range(10, 55, 5), 'multiplier': range(20, 35, 5), 'logging': False}
    },

    '5c188831-8cea-43f6-b3d1-9ced5505ce8d': {
        'strategy': HighLowClassic_Long_D,
        'params': {'period': range(10, 55, 5), 'logging': False}
    },

    'cf264e4d-f3b8-414a-9975-3ccf1bcacbd5': {
        'strategy': HighLowMiddle_Long_D,
        'params': {'period': range(10, 55, 5), 'logging': False}
    }
}

tickers = [
    "CBOM",
    "ALRS",
    "VTBR",
    "MDMG",
    "GEMC",
    "VKCO",
    "LENT",
    "RUAL",
    "T",
    "HEAD",
    "CNRU",
    "ENPG",
    "YDEX",
    "BSPB",
    "AQUA",
    "AFKS",
    "AFLT",
    "VSEH",
    "GAZP",
    "GMKN",
    "RAGR",
    "LSRG",
    "POSI",
    "RENI",
    "EUTR",
    "IRAO",
    "X5",
    "LEAS",
    "MVID",
    "MBNK",
    "MAGN",
    "MTLR",
    "MTLRP",
    "MTSS",
    "MOEX",
    "LKOH",
    "BELU",
    "NLMK",
    "PIKK",
    "PLZL",
    "RTKM",
    "RTKMP",
    "SBER",
    "SBERP",
    "CHMF",
    "SELG",
    "SVCB",
    "FLOT",
    "TGKA",
    "TRNFP",
    "HYDR",
    "FEES",
    "PHOR",
    "ELFV",
    "SFIN",
    "UPRO",
    "ASTR",
    "SGZH",
    "RNFT",
    "MSNG",
    "SMLT",
    "NVTK",
    "ROSN",
    "TATN",
    "TATNP"
]
