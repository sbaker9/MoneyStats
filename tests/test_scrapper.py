import unittest
import scrapper


class ScrapperTests(unittest.TestCase):

    def test_get_dataframe_from_csv_file(self):
        balance_sheet_df = scrapper.get_dataframe_from_csv_file('../data/nflx_balance_sheet.csv')
        # 30 rows x 4 columns
        self.assertEqual(balance_sheet_df.shape, (30, 4))

    def test_dollars(self):
        # use assertAlmostEqual instead of assertEqual to allow for float tolerance
        self.assertAlmostEqual(scrapper.dollars('$123.45'), 123.45)
        self.assertAlmostEqual(scrapper.dollars('$(123.45)'), -123.45)

        self.assertAlmostEqual(scrapper.dollars('$123,456,789)'), 123456789)

    def test_get_dataframe_from_file(self):
        """
        unit test passes, but get_dataframe_from_html_file throws warning
        ../Users/stevebaker/anaconda3/envs/beepscore/lib/python3.6/importlib/_bootstrap.py:219:
            ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__
        https://github.com/wireservice/csvkit/issues/937
        """
        income_df = scrapper.get_dataframe_from_html_file('../data/nflx_income.html')
        # 18 rows x 4 columns
        self.assertEqual(income_df.shape, (18, 4))

    def test_get_net_income(self):

        df = scrapper.get_dataframe_from_csv_file('../data/nflx_income.csv')
        net_income = scrapper.get_net_income(df)
        self.assertAlmostEqual(net_income.iloc[0], 1211242.0)
        self.assertAlmostEqual(net_income.iloc[1], 558929.0)
        self.assertAlmostEqual(net_income.iloc[2], 186678.0)
        self.assertAlmostEqual(net_income.iloc[3], 122641.0)

    def test_get_revenue(self):
        """
        unit test passes, but get_dataframe_from_html_file throws warning
        ../Users/stevebaker/anaconda3/envs/beepscore/lib/python3.6/importlib/_bootstrap.py:219:
            ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__
        https://github.com/wireservice/csvkit/issues/937
        """

        df = scrapper.get_dataframe_from_html_file('../data/nflx_income.html')
        revenue = scrapper.get_revenue(df)
        self.assertAlmostEqual(revenue.iloc[0], 15794341.0)
        self.assertAlmostEqual(revenue.iloc[1], 11692713.0)
        self.assertAlmostEqual(revenue.iloc[2], 8830669.0)
        self.assertAlmostEqual(revenue.iloc[3], 6779511.0)

    def test_get_equity(self):
        df = scrapper.get_dataframe_from_csv_file('../data/nflx_balance_sheet.csv')
        equity = scrapper.get_equity(df)
        self.assertAlmostEqual(equity.iloc[0], 5238765.0)

    def test_get_total_liabilities(self):
        df = scrapper.get_dataframe_from_csv_file('../data/nflx_balance_sheet.csv')
        total_liabilities = scrapper.get_total_liabilities(df)
        self.assertAlmostEqual(total_liabilities.iloc[0], 20735635.0)
        self.assertAlmostEqual(total_liabilities.iloc[1], 15430786.0)
        self.assertAlmostEqual(total_liabilities.iloc[2], 10906810.0)
        self.assertAlmostEqual(total_liabilities.iloc[3], 7979445.0)

    def test_get_roic(self):
        income_df = scrapper.get_dataframe_from_csv_file('../data/nflx_income.csv')
        balance_sheet_df = scrapper.get_dataframe_from_csv_file('../data/nflx_balance_sheet.csv')
        roic = scrapper.get_roic(income_df, balance_sheet_df)
        self.assertAlmostEqual(roic.iloc[0], 0.046632145497104843)
        self.assertAlmostEqual(roic.iloc[1], 0.029397600830011788)
        self.assertAlmostEqual(roic.iloc[2], 0.013739851221165545)
        self.assertAlmostEqual(roic.iloc[3], 0.012020244105801201)


if __name__ == '__main__':
    unittest.main()
