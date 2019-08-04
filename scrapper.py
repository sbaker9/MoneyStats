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


def get_dataframe(url, css_id):
    """
    :param url: url to load
    :param css_id: id of element to select
    :return: dataframe
    """

    # to read from local data file, uncomment these.
    # this can be handy during development
    # dataframes = pd.read_html('./data/html.html', header=0, index_col=0, skiprows=0)

    # to read from web, uncomment these
    html = get_html(url, css_id)
    print('html:\n', html)
    dataframes = pd.read_html(html, header=0, index_col=0, skiprows=0)

    # read_html returns a list of dataframes, get the first one
    df = dataframes[0]

    df = cleaned_df(df)

    return df


def cleaned_df(df):
    """
    :param df: dataframe from read_html
    :return: dataframe with 4 columns containing amounts in thousands of dollars $000
    """
    # drop rows with all values NaN (Not A Number)
    df = df.dropna(how='all')

    # print(df.columns.values)
    # get desired column names. The values may change over time.
    column_names = df.columns.values[1:5]
    print(column_names)
    # ['12/31/2018' '12/31/2017' '12/31/2016' '12/31/2015']

    # the dollar amounts are in columns "Unnamed:25 through Unnamed:28
    # slice to keep columns with dollar amounts
    df = df.loc[:, "Unnamed: 25": 'Unnamed: 28']
    # re-add column names
    df.columns = column_names

    return df


if __name__ == '__main__':

    stock_symbol = 'nflx'
    url = url(stock_symbol)
    print(url)

    css_id = 'financials-iframe-wrap'

    df = get_dataframe(url, css_id)
    # write dataframe to a csv file
    df.to_csv('./data/data.csv')

    print(df)

    # pandas loc slice [:, 0:1] gets all rows, columns 0 through 1 inclusive
    newest_year_df = df.iloc[:, 0:1]
    revenue = newest_year_df.loc['Total Revenue', :].values[0]
    print(revenue)
