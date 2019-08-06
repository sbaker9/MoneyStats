import unittest
import url_constructor


class FilenameConstructorTests(unittest.TestCase):

    def test_get_balance_sheet_url(self):
        self.assertEqual(url_constructor.get_balance_sheet_url('nflx'),
                         'https://www.nasdaq.com/symbol/nflx/financials?query=balance-sheet')

    def test_get_income_url(self):
        self.assertEqual(url_constructor.get_income_url('nflx'), 'https://www.nasdaq.com/symbol/nflx/financials')


if __name__ == '__main__':
    unittest.main()
