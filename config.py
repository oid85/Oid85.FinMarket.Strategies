from strategies.CloseCrossSma_Long_D.CloseCrossSma_Long_D import CloseCrossSma_Long_D
from strategies.HmaInclination_Long_D.HmaInclination_Long_D import HmaInclination_Long_D
from strategies.Supertrend_Long_D.Supertrend_Long_D import Supertrend_Long_D

host = '26.147.25.39'
port = 5432
database = 'finmarket_prod'
user = 'postgres'
password = 'postgres'

start_date = '2022-01-01'
end_date = '2025-12-31'

portfolio_money = 1000000.0
percent_size = 50

optimization_result_filter = {
    'sharp_ratio': 2.0,
    'profit_factor': 2.0,
    'recovery_factor': 2.0,
    'max_drawdown_percent': 20.0,
}

strategies = {
    '208e13f2-7609-4d5c-832e-71fa75319c22': {
        'strategy': CloseCrossSma_Long_D,
        'params': {'period': range(10, 100, 5), 'logging': False}
    },

    '41b8cba8-8d1b-4a42-867b-03e798d888ad': {
        'strategy': HmaInclination_Long_D,
        'params': {'period': range(10, 100, 5), 'logging': False}
    },

    '1031b21c-1439-4a9c-aea3-f389039d157b': {
        'strategy': Supertrend_Long_D,
        'params': {'period': range(10, 100, 5), 'multiplier': range(20, 30, 2), 'logging': False}
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
