# pip install pandas-datareader
# https://pandas-datareader.readthedocs.io/en/latest/

import pandas_datareader.data as web
import datetime as dt

def get_pandas_naver_data(id, start, end):
    _df = web.DataReader(id, "naver", start=start, end=end)
    return _df

def get_pandas_stooq_data(id, start, end):
    _df = web.DataReader(id, "stooq", start=start, end=end)
    return _df


def get_pandas_fred_data(id):
    return web.get_data_fred(id)


if "__main__" == __name__:
    df = get_pandas_naver_data('005930', '2025-01-01', '2025-01-20')
    print(df.head())

    start_date = dt.datetime(2025, 1, 1)
    end_date = dt.datetime(2025, 1, 20)

    df = get_pandas_stooq_data('AAPL', start_date, end_date)
    print(df.head())

    df = get_pandas_fred_data("UNRATE")
    print(df.head())