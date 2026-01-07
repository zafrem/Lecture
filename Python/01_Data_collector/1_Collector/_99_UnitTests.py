#pip install unittest

import unittest
import _1_API_Stock_Funds_yfinance as ystock
import _2_API_Stock_pandas_datareader as pstock
import _3_API_AltCoin_binance as altcoin
import _4_RSS_Trend_Keyword_Google_trend as google_trend
import _5_Scraping_Trend_Keyword_Blackkiwi as rss_trend
import _5_Scraping_Spot_NFL as nfl
import _7_Scraping_Spot_Premier_League as premier_league
import _8_Scraping_Weather_windy as weather


class data_getter:
    def _ystock_1(self, target):
        return ystock.get_stock_data_ticker(target)

    def _ystock_2(self, target):
        return ystock.get_stock_data_download(target)

    def _ystock_3(self, target):
        return ystock.get_funds_data_ticker(target)

    def _pstock_1(self):
        return pstock.get_pandas_naver_data('005930', '2025-01-01', '2025-01-20')

    def _pstock_2(self):
        import datetime as dt
        start_date = dt.datetime(2025, 1, 1)
        end_date = dt.datetime(2025, 1, 20)
        return pstock.get_pandas_stooq_data('AAPL', start_date, end_date)

    def _altcoin(self):
        return altcoin.get_altcoin_data()

    def _google_trend(self, target):
        return google_trend.get_trend(target)

    def _blackkiwi_trend(self):
        return rss_trend.get_keyword()

    def _nfl(self):
        return nfl.get_nfl_schedules()

    def _premier_league(self):
        return premier_league.get_keyword()

    def _weather(self):
        return weather.get_keyword()

class PlusTest(unittest.TestCase):
    def setUp(self):
        self.data_getter = data_getter()

    def test_stock(self):
        self.assertIsNotNone(self.data_getter._ystock_1("MSFT"))
        self.assertIsNotNone(self.data_getter._ystock_2("AAPL"))
        self.assertIsNotNone(self.data_getter._ystock_3("SPY"))
        self.assertIsNotNone(self.data_getter._pstock_1())
        self.assertIsNotNone(self.data_getter._pstock_2())

    def test_altcoin(self):
        self.assertIsNotNone(self.data_getter._altcoin())

    def test_trend_google(self):
        self.assertIn('[Google Trend - KR]', self.data_getter._google_trend('KR'))

    def test_trend_blackkiwi(self):
        self.assertIn('1.', self.data_getter._blackkiwi_trend())

    def test_nfl(self):
        self.assertTrue(self.data_getter._nfl())

    def test_premier_league(self):
        self.assertTrue(self.data_getter._premier_league())

    def test_weather(self):
        self.assertIn('Time', self.data_getter._weather())


if __name__ == '__main__':
    unittest.main()