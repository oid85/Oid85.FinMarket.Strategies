import psycopg2 as ps
import pandas as pd
import config


def get_daily_candles_by_ticker(ticker, start_date, end_date):
    connection = ps.connect(host=config.host, port=config.port, database=config.database, user=config.user,
                            password=config.password)
    sql = f"select date as datetime, open, close, high, low, volume from storage.daily_candles where instrument_id in (select instrument_id from public.instruments where ticker = '{ticker}') and date >= '{start_date}' and date <= '{end_date}' order by date"
    df = pd.read_sql(sql, con=connection)

    return df


def get_five_minute_candles_by_ticker(ticker, start_date, end_date):
    connection = ps.connect(host=config.host, port=config.port, database=config.database, user=config.user,
                            password=config.password)
    sql = f"select date as datetime, time, open, close, high, low, volume from storage.five_minute_candles where instrument_id in (select instrument_id from public.instruments where ticker = '{ticker}') and date >= '{start_date}' and date <= '{end_date}' order by datetime"
    df = pd.read_sql(sql, con=connection)

    return df
