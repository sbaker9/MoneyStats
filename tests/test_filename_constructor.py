import unittest
import filename_constructor
from pathlib import Path


class FilenameConstructorTests(unittest.TestCase):

    def test_get_balance_sheet_csv_filename(self):
        path = filename_constructor.get_balance_sheet_csv_filename('nflx')
        self.assertEqual(path, Path('./data/nflx_balance_sheet.csv'))
        self.assertEqual(path.parent, Path('data'))
        self.assertEqual(path.anchor, '')
        self.assertEqual(path.name, 'nflx_balance_sheet.csv')
        self.assertEqual(path.stem, 'nflx_balance_sheet')
        self.assertEqual(path.suffix, '.csv')

        self.assertEqual(filename_constructor.get_balance_sheet_csv_filename('appl'), Path('./data/appl_balance_sheet.csv'))

    def test_get_income_csv_filename(self):
        self.assertEqual(filename_constructor.get_income_csv_filename('nflx'), Path('./data/nflx_income.csv'))
        self.assertEqual(filename_constructor.get_income_csv_filename('appl'), Path('./data/appl_income.csv'))

    def test_get_income_html_filename(self):
        self.assertEqual(filename_constructor.get_income_html_filename('nflx'), Path('./data/nflx_income.html'))
        self.assertEqual(filename_constructor.get_income_html_filename('appl'), Path('./data/appl_income.html'))


if __name__ == '__main__':
    unittest.main()
