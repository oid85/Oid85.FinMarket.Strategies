import json
import datetime
import psycopg2 as ps
import pandas as pd
import config
import hashlib


def get_database_connection():
    return ps.connect(host=config.host, port=config.port, database=config.database, user=config.user, password=config.password)

def get_daily_candles_by_ticker(ticker, start_date, end_date):
    '''Получение дневных свечей по тикеру'''

    connection = get_database_connection()

    sql = (f"select date as datetime, open, high, low, close, volume "
           f"from storage.daily_candles "
           f"where instrument_id in (select instrument_id from public.instruments where ticker = '{ticker}') "
           f"and date >= '{start_date}' "
           f"and date <= '{end_date}' "
           f"order by date")

    df = pd.read_sql(sql, con=connection, parse_dates={"datetime": {"format": "%Y-%m-%d"}})
    connection.close()

    return df


def clear_optimization_result():
    '''Очищение результатов оптимизации'''
    return None


def is_exists_optimization_result(settings, params_md5):
    pass


def save_optimization_result(ticker, settings, results):
    '''Сохранение результатов оптимизации'''

    connection = get_database_connection()
    cursor = connection.cursor()

    strategy_version = settings['version']
    strategy_id = settings['id']

    for result in results:
        sharpe = result[0].analyzers.sharpe.get_analysis()
        drawdown = result[0].analyzers.drawdown.get_analysis()
        trades = result[0].analyzers.trades.get_analysis()
        strategy_params = json.dumps(*result[0].params)
        strategy_params_hash = hashlib.md5(strategy_params.encode()).hexdigest()
        total = trades.total.total
        total_open = trades.open
        total_closed = trades.closed
        streak_won_longest = trades.streak.won.longest
        streak_lost_longest = trades.streak.lost.longest
        pnl_net_total = trades.pnl.net.total
        pnl_net_average = trades.pnl.net.average
        max_drawdown_percent = drawdown.max.drawdown
        profit_factor = 0
        recovery_factor = 0
        sharp_ratio = sharpe.sharperatio

        datetime_now = datetime.datetime.now().isoformat()
        datetime_min = datetime.datetime(1, 1, 1, 0, 0, 0).isoformat()

        if is_exists_optimization_result(settings, strategy_params_hash):
            sql = (f"update storage.optimization_results "
                   f"set "
                   f"total={total}, "
                   f"total_open={total_open}, "
                   f"total_closed={total_closed}, "
                   f"streak_won_longest={streak_won_longest}, "
                   f"streak_lost_longest={streak_lost_longest}, "
                   f"pnl_net_total={pnl_net_total}, "
                   f"pnl_net_average={pnl_net_average}, "
                   f"max_drawdown_percent={max_drawdown_percent}, "
                   f"profit_factor={profit_factor}, "
                   f"recovery_factor={recovery_factor}, "
                   f"sharp_ratio={sharp_ratio}, "                   
                   f"updated_at='{datetime_now}', "                   
                   f"where strategy_id={strategy_id} "
                   f"and  strategy_version={strategy_version} "
                   f"and  strategy_params_hash={strategy_params_hash}")
        else:
            sql = (f"insert into storage.optimization_results ("
                   f"id, ticker, timeframe, strategy_id, strategy_version, "
                   f"strategy_params, strategy_params_hash, total, total_open, total_closed, "
                   f"streak_won_longest, streak_lost_longest, pnl_net_total, pnl_net_average, "
                   f"max_drawdown_percent, profit_factor, recovery_factor, sharp_ratio, "
                   f"created_at, updated_at, deleted_at, is_deleted) "
                   f"values(gen_random_uuid(), '{ticker}', '{settings.timeframe}', '{settings.id}', {settings.version}, "
                   f"'{strategy_params}', '{strategy_params_hash}', {total}, {total_open}, {total_closed}, "
                   f"{streak_won_longest}, {streak_lost_longest}, {pnl_net_total}, {pnl_net_average}, "
                   f"{max_drawdown_percent}, {profit_factor}, {recovery_factor}, {sharp_ratio}, "
                   f"'{datetime_now}', '{datetime_min}', '{datetime_min}', false)")

        cursor.execute(sql)

    connection.commit()
    cursor.close()
    connection.close()


def get_backtest_strategies():
    '''Получение стратегий для бэктеста'''
    return None


def calculate_positions():
    '''Расчет позиций инструментов на основе данных бэектеста'''
    return None