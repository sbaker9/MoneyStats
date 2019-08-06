import unittest
import filename_constructor


class FilenameConstructorTests(unittest.TestCase):

    def test_get_balance_sheet_csv_filename(self):
        self.assertEqual(filename_constructor.get_balance_sheet_csv_filename('nflx'), './data/nflx_balance_sheet.csv')
        self.assertEqual(filename_constructor.get_balance_sheet_csv_filename('appl'), './data/appl_balance_sheet.csv')

    def test_get_income_csv_filename(self):
        self.assertEqual(filename_constructor.get_income_csv_filename('nflx'), './data/nflx_income.csv')
        self.assertEqual(filename_constructor.get_income_csv_filename('appl'), './data/appl_income.csv')

    def test_get_income_html_filename(self):
        self.assertEqual(filename_constructor.get_income_html_filename('nflx'), './data/nflx_income.html')
        self.assertEqual(filename_constructor.get_income_html_filename('appl'), './data/appl_income.html')


if __name__ == '__main__':
    unittest.main()