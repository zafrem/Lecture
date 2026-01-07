#pip install unittest

import unittest
import _1_File_plantext as _plantext
import _2_File_json as _json
import _3_SQLite as _sqlite
import _4_SQLAlchemy as _sql_alchemy

class data_class:
    def plantext_data_save(self, target):
        return _plantext.save_data_text()

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