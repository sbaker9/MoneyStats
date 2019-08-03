#!/usr/bin/env python3

from io import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd


"""
reference websearcher browser_driver.py
https://github.com/beepscore/websearcher
"""


def url(stock_symbol):
    """
    return string representing url
    e.g. 'https://www.nasdaq.com/symbol/nflx/financials'
    """
    base_url = 'https://www.nasdaq.com'
    path = '/symbol/' + stock_symbol + '/financials'

    url_string = base_url + path
    return url_string


def get_text(url, css_id):
    """
    Uses browser to request info.
    Waits for javascript to run and return html. Selects by css_id.
    :param url: url to load
    :param css_id: id of page html element to select
    return string. return empty string if timeout or error
    """

    browser = webdriver.Chrome()

    browser.get(url)

    try:
        # http://stackoverflow.com/questions/37422832/waiting-for-a-page-to-load-in-selenium-firefox-w-python?lq=1
        # http://stackoverflow.com/questions/5868439/wait-for-page-load-in-selenium
        WebDriverWait(browser, 20).until(lambda d: d.find_element_by_id(css_id).is_displayed())
        element = browser.find_element_by_id(css_id)
        return element.text

    except TimeoutException:
        print("TimeoutException, returning empty string")
        return ""

    except AttributeError:
        # http://stackoverflow.com/questions/9823936/python-how-do-i-know-what-type-of-exception-occured#9824050
        print("AttributeError, returning empty string")
        return ""

    finally:
        browser.quit()


def get_dataframe(url, css_id, column_names):
    """
    :param url: url to load
    :param css_id: id of element to select
    :param column_names: column names for dataframe
    :return: dataframe
    """

    # read from local data file
    # this can be handy during development
    # df = pd.read_csv('./data/data.txt', sep=' ', names=column_names, skiprows=10)

    # read from web
    text = get_text(url, css_id)
    # https://stackoverflow.com/questions/20696479/pandas-read-csv-from-string-or-package-data
    df = pd.read_csv(StringIO(text), dtype=object, sep=' ', names=column_names, skiprows=10)

    return df


if __name__ == '__main__':

    stock_symbol = 'nflx'
    url = url(stock_symbol)
    print(url)

    css_id = 'left-column-div'

    #data = get_text(url, css_id)
    #print(data)

    column_names = []

    df = get_dataframe(url, css_id, column_names)
    print(df)


