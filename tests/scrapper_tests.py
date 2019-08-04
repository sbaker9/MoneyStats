import unittest
import scrapper


class ScrapperTests(unittest.TestCase):

    def test_get_html_filename(self):
        self.assertEqual(scrapper.get_html_filename('nflx'), './data/nflx.html')
        self.assertEqual(scrapper.get_html_filename('appl'), './data/appl.html')

    def test_get_income_url(self):
        self.assertEqual(scrapper.get_income_url('nflx'), 'https://www.nasdaq.com/symbol/nflx/financials')

    def test_get_balance_sheet_url(self):
        self.assertEqual(scrapper.get_balance_sheet_url('nflx'),
                         'https://www.nasdaq.com/symbol/nflx/financials?query=balance-sheet')

    def test_get_dataframe_from_file(self):
        df = scrapper.get_dataframe_from_file('../data/nflx.html')
        # 18 rows x 4 columns
        self.assertEqual(df.shape, (18, 4))

    def test_dollars(self):
        # use assertAlmostEqual instead of assertEqual to allow for float tolerance
        self.assertAlmostEqual(scrapper.dollars('$123.45'), 123.45)
        self.assertAlmostEqual(scrapper.dollars('$(123.45)'), -123.45)

        self.assertAlmostEqual(scrapper.dollars('$123,456,789)'), 123456789)

    def test_get_revenue(self):
        df = scrapper.get_dataframe_from_file('../data/nflx.html')
        revenue = scrapper.get_revenue(df)
        self.assertAlmostEqual(revenue, 15794341.0)


if __name__ == '__main__':
    unittest.main()
