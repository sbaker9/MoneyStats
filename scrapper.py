
#!/usr/bin/env python3

'''
from io import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd
'''

"""
reference websearcher browser_driver.py
https://github.com/beepscore/websearcher
"""


def url(stock_symbol):
    """
    date_string of the form ddMONyyyy e.g. 25OCT2018, 31JAN2019
    When requesting options, must be in the future.
    Must be a valid option expiration date for that stock.
    return url
    """
    base_url = 'https://www.nasdaq.com'
    path = '/symbol/' + stock_symbol + '/financials'

    url_string = base_url + path
    return url_string

if __name__ == '__main__':

    stock_symbol = 'nflx'
    url = url(stock_symbol)
    print(url)


