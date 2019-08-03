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


def get_html(url, css_id):
    """
    Uses browser to request info.
    Waits for javascript to run and return html. Selects by css_id.
    :param url: url to load
    :param css_id: id of page html element to select
    return html. return empty string if timeout or error
    """

    browser = webdriver.Chrome()

    browser.get(url)

    try:
        # http://stackoverflow.com/questions/37422832/waiting-for-a-page-to-load-in-selenium-firefox-w-python?lq=1
        # http://stackoverflow.com/questions/5868439/wait-for-page-load-in-selenium

        # alternatively select by a class, may be useful if a unique div is not available.
        # WebDriverWait(browser, 20).until(lambda d: d.find_elements_by_class_name(css_selector).is_displayed())
        # element = browser.find_elements_by_class_name(css_selector)[0]

        WebDriverWait(browser, 20).until(lambda d: d.find_element_by_id(css_id).is_displayed())
        element = browser.find_element_by_id(css_id)

        html = element.get_attribute('innerHTML')
        return html

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

    # to read from local data file, uncomment these.
    # this can be handy during development
    dataframes = pd.read_html('./data/html.html', header=0, index_col=0, skiprows=0)

    # FIXME: html has dollar amounts but dataframes don't

    # to read from web, uncomment these
    # html = get_html(url, css_id)
    # print('html:\n', html)
    # dataframes = pd.read_html(html, header=0, index_col=0, skiprows=0)

    # read_html returns a list of dataframes, get the first one
    df = dataframes[0]

    # slice first 6 columns. careful this deleted dollar amounts!
    # df = df.iloc[:, 0:5]

    return df


if __name__ == '__main__':

    stock_symbol = 'nflx'
    url = url(stock_symbol)
    print(url)

    css_id = 'financials-iframe-wrap'

    column_names = []

    df = get_dataframe(url, css_id, column_names)
    # write dataframe to a csv file
    df.to_csv('./data/data.csv')

    print(df)


