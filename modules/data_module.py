import json
import datetime
import psycopg2 as ps
import pandas as pd
import config
import hashlib
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

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
    connection = get_database_connection()
    cursor = connection.cursor()
    sql = 'delete from storage.optimization_results'
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


def clear_backtest_result():
    '''Очищение результатов бэктеста'''
    connection = get_database_connection()
    cursor = connection.cursor()
    sql = 'delete from storage.backtest_results'
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


def clear_strategy_signals():
    '''Очищение таблицы позиций'''
    connection = get_database_connection()
    cursor = connection.cursor()

    sql = 'delete from storage.strategy_signals'
    cursor.execute(sql)
    connection.commit()

    datetime_now = datetime.datetime.now().isoformat()
    datetime_min = datetime.datetime(1, 1, 1, 0, 0, 0).isoformat()

    for ticker in config.tickers:
        sql = (f"insert into storage.strategy_signals ("
               f"ticker, position, created_at, updated_at, deleted_at, is_deleted) "
               f"values('{ticker}', 0, '{datetime_now}', '{datetime_min}', '{datetime_min}', false)")
        cursor.execute(sql)

    connection.commit()
    cursor.close()
    connection.close()


def get_good_optimization_results():
    connection = get_database_connection()

    sql = (f"select id, ticker, strategy_id, strategy_params, "
           f"sharp_ratio, profit_factor, recovery_factor, max_drawdown_percent "
           f"from storage.optimization_results " 
           f"where sharp_ratio >= {config.optimization_result_filter['sharp_ratio']} " 
           f"and profit_factor >= {config.optimization_result_filter['profit_factor']} " 
           f"and recovery_factor >= {config.optimization_result_filter['recovery_factor']} " 
           f"and max_drawdown_percent <= {config.optimization_result_filter['max_drawdown_percent']}")

    df = pd.read_sql(sql, con=connection)
    connection.close()

    return df


def save_results(ticker, settings, results, table_name):
    '''Сохранение результатов оптимизации'''
    connection = get_database_connection()
    cursor = connection.cursor()

    strategy_version = settings['version']
    strategy_id = settings['id']
    strategy_timeframe = settings['timeframe']

    for result in results:
        try:
            sharpe = result[0].analyzers.sharpe.get_analysis()
            drawdown = result[0].analyzers.drawdown.get_analysis()
            trades = result[0].analyzers.trades.get_analysis()
            strategy_params = json.dumps(result[0].p._getkwargs())
            strategy_params_hash = hashlib.md5(strategy_params.encode()).hexdigest()
            total = trades.total.total
            total_open = trades.total.open
            total_closed = trades.total.closed
            streak_won_longest = trades.streak.won.longest
            streak_lost_longest = trades.streak.lost.longest
            pnl_net_total = trades.pnl.net.total
            pnl_net_average = trades.pnl.net.average
            max_drawdown_percent = drawdown.max.drawdown
            profit_factor = abs(trades.won.pnl.total / trades.lost.pnl.total)
            recovery_factor = trades.pnl.net.total / drawdown.max.moneydown
            sharp_ratio = sharpe['sharperatio']

            datetime_now = datetime.datetime.now().isoformat()
            datetime_min = datetime.datetime(1, 1, 1, 0, 0, 0).isoformat()

            sql = (f"insert into storage.{table_name} ("
                   f"ticker, timeframe, strategy_id, strategy_version, "
                   f"strategy_params, strategy_params_hash, total, total_open, total_closed, "
                   f"streak_won_longest, streak_lost_longest, pnl_net_total, pnl_net_average, "
                   f"max_drawdown_percent, profit_factor, recovery_factor, sharp_ratio, "
                   f"created_at, updated_at, deleted_at, is_deleted) "
                   f"values('{ticker}', '{strategy_timeframe}', '{strategy_id}', {strategy_version}, "
                   f"'{strategy_params}', '{strategy_params_hash}', {total}, {total_open}, {total_closed}, "
                   f"{streak_won_longest}, {streak_lost_longest}, {pnl_net_total}, {pnl_net_average}, "
                   f"{max_drawdown_percent}, {profit_factor}, {recovery_factor}, {sharp_ratio}, "
                   f"'{datetime_now}', '{datetime_min}', '{datetime_min}', false)")

            cursor.execute(sql)

        except:
            pass

    connection.commit()
    cursor.close()
    connection.close()


def save_optimization_results(ticker, settings, results):
    save_results(ticker, settings, results, 'optimization_results')


def save_backtest_results(ticker, settings, results):
    save_results(ticker, settings, results, 'backtest_results')


def get_strategy_by_id(strategy_id):
    for strategy in config.strategies.keys():
        if strategy.settings['id'] == strategy_id:
            return strategy
    return None


def get_backtest_strategies():
    '''Получение стратегий для бэктеста'''
    backtest_strategies = {}

    df = get_good_optimization_results()

    for i, row in df.iterrows():
        ticker = row['ticker']
        strategy = get_strategy_by_id(row['strategy_id'])
        params = row['strategy_params']
        strategy_data = {'strategy': strategy, 'ticker': ticker, 'params': params}
        backtest_strategies[row['id']] = strategy_data

    return backtest_strategies


def save_strategy_signals():
    '''Расчет позиций инструментов на основе данных бэктеста'''
    connection = get_database_connection()
    cursor = connection.cursor()

    for ticker in config.tickers:
        cursor.execute(
            f"update storage.strategy_signals "
            f"set position = coalesce((select sum(total_open) from storage.backtest_results where ticker = '{ticker}'), 0) "
            f"where ticker = '{ticker}'")

    connection.commit()
    cursor.close()
    connection.close()