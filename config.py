from strategies.CloseCrossSma_Long_D import CloseCrossSma_Long_D
from strategies.HmaInclination_Long_D.HmaInclination_Long_D import HmaInclination_Long_D

host = '26.147.25.39'
port = 5432
database = 'finmarket_prod'
user = 'postgres'
password = 'postgres'

start_date = '2022-01-01'
end_date = '2024-12-31'

out_start_date = '2024-01-01'
out_end_date = '2025-12-31'

strategy_money = 1000000.0
percent_size = 50

optimization_result_filter = {
    'sharp_ratio': 2.0,
    'profit_factor': 2.0,
    'recovery_factor': 2.0,
    'max_drawdown_percent': 20.0,
}

strategies = {
    CloseCrossSma_Long_D: {'period': range(10, 50, 5), 'logging': False},
    HmaInclination_Long_D: {'period': range(10, 50, 5), 'logging': False}
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
