import unittest
import scrapper


class ScrapperTests(unittest.TestCase):

    def test_get_balance_sheet_csv_filename(self):
        self.assertEqual(scrapper.get_balance_sheet_csv_filename('nflx'), './data/nflx_balance_sheet.csv')
        self.assertEqual(scrapper.get_balance_sheet_csv_filename('appl'), './data/appl_balance_sheet.csv')

    def test_get_balance_sheet_url(self):
        self.assertEqual(scrapper.get_balance_sheet_url('nflx'),
                         'https://www.nasdaq.com/symbol/nflx/financials?query=balance-sheet')

    def test_get_income_csv_filename(self):
        self.assertEqual(scrapper.get_income_csv_filename('nflx'), './data/nflx_income.csv')
        self.assertEqual(scrapper.get_income_csv_filename('appl'), './data/appl_income.csv')

    def test_get_income_html_filename(self):
        self.assertEqual(scrapper.get_income_html_filename('nflx'), './data/nflx_income.html')
        self.assertEqual(scrapper.get_income_html_filename('appl'), './data/appl_income.html')

    def test_get_income_url(self):
        self.assertEqual(scrapper.get_income_url('nflx'), 'https://www.nasdaq.com/symbol/nflx/financials')

    def test_get_dataframe_from_csv_file(self):
        balance_sheet_df = scrapper.get_dataframe_from_csv_file('../data/nflx_balance_sheet.csv')
        # 30 rows x 4 columns
        self.assertEqual(balance_sheet_df.shape, (30, 4))

    def test_get_dataframe_from_file(self):
        income_df = scrapper.get_dataframe_from_html_file('../data/nflx_income.html')
        # 18 rows x 4 columns
        self.assertEqual(income_df.shape, (18, 4))

    def test_dollars(self):
        # use assertAlmostEqual instead of assertEqual to allow for float tolerance
        self.assertAlmostEqual(scrapper.dollars('$123.45'), 123.45)
        self.assertAlmostEqual(scrapper.dollars('$(123.45)'), -123.45)

        self.assertAlmostEqual(scrapper.dollars('$123,456,789)'), 123456789)

    def test_get_revenue(self):
        df = scrapper.get_dataframe_from_html_file('../data/nflx_income.html')
        revenue = scrapper.get_revenue(df)
        self.assertAlmostEqual(revenue, 15794341.0)

    def test_get_equity(self):
        df = scrapper.get_dataframe_from_csv_file('../data/nflx_balance_sheet.csv')
        equity = scrapper.get_equity(df)
        self.assertAlmostEqual(equity, 5238765.0)


if __name__ == '__main__':
    unittest.main()
