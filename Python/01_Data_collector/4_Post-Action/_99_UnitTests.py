#pip install unittest

import unittest
import _1_technical_analysis_AROON as _aroon
import _1_technical_analysis_Bollinger_band as _bollinger
import _1_technical_analysis_Envelope as _envelope
import _1_technical_analysis_MACD as macd
import _1_technical_analysis_Stochastic as stochastic
import _2_Create_word_file
import _3_Create_excel_file
import _4_Gmail_Report
import _5_Telegram_bot

class data_class:
    def plantext_data_save(self, target):
        return _aroon

    def plantext_data_load(self, target):
        return _plantext.load_data_text()


class PlusTest(unittest.TestCase):
    def setUp(self):
        self._data = data_class()

    #def test_stock(self):
    #    self.assertIn("Tesla", self.scraping._stock("Tesla"))

    #def test_altcoin(self):
    #    self.assertIn("dogecoin", self.scraping._altcoin("dogecoin"))



if __name__ == '__main__':
    unittest.main()