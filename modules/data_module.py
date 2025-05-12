import psycopg2 as ps
import pandas as pd
import config


def get_daily_candles_by_ticker(ticker, start_date, end_date):
    connection = ps.connect(host=config.host,
                            port=config.port,
                            database=config.database,
                            user=config.user,
                            password=config.password)
    sql = (f"select date as datetime, open, high, low, close, volume "
           f"from storage.daily_candles "
           f"where instrument_id in (select instrument_id from public.instruments where ticker = '{ticker}') "
           f"and date >= '{start_date}' "
           f"and date <= '{end_date}' "
           f"order by date")

    df = pd.read_sql(
        sql,
        con=connection,
        parse_dates={"datetime": {"format": "%Y-%m-%d"}}
    )

    return df


def get_five_minute_candles_by_ticker(ticker, start_date, end_date):
    connection = ps.connect(host=config.host, port=config.port, database=config.database, user=config.user,
                            password=config.password)
    sql = (f"select concat(date, ' ', time) as datetime, open, high, low, close, volume "
           f"from storage.five_minute_candles "
           f"where instrument_id in (select instrument_id from public.instruments where ticker = '{ticker}') "
           f"and date >= '{start_date}' "
           f"and date <= '{end_date}' "
           f"order by datetime")

    df = pd.read_sql(sql, con=connection)

    return df
