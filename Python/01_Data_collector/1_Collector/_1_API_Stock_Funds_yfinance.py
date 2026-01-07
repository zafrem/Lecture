# pip install yfinance
# https://pypi.org/project/yfinance/

import yfinance as yf


def get_stock_data_ticker(target):
    _msft = yf.Ticker(target)
    return _msft


def get_stock_data_download(target):
    _aapl = yf.download(target)
    return _aapl


def get_funds_data_ticker(target):
    _spy = yf.Ticker(target).funds_data
    return _spy


if "__main__" == __name__:
    msft = get_stock_data_ticker("MSFT")
    print(msft.info)
    print(msft.calendar)
    print(msft.analyst_price_targets)
    print(msft.quarterly_income_stmt)
    print(msft.history(period='1mo'))
    print(msft.option_chain(msft.options[0]).calls)

    aapl = get_stock_data_download('AAPL')
    print(aapl.head())

    spy = get_funds_data_ticker('SPY')
    print(spy.description)
    print(spy.top_holdings)