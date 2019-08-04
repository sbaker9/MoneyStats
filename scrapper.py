#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd


"""
reference websearcher browser_driver.py
https://github.com/beepscore/websearcher
"""

# css id used to select html containing table within page html. Includes a little additional html
css_id = 'financials-iframe-wrap'


def get_income_html_filename(stock_symbol):
    """
    :param stock_symbol: used to construct the html data filename, e.g. 'nflx'
    :return: string representing filename
    e.g. './data/<stock_symbol>.html', './data/nflx_income.html'
    """
    path = './data/' + stock_symbol + '_income.html'
    return path


def get_income_url(stock_symbol):
    """
    :param stock_symbol: e.g. 'nflx'
    :return: string representing url for income
    e.g. 'https://www.nasdaq.com/symbol/nflx/financials'
    """
    base_url = 'https://www.nasdaq.com'
    path = '/symbol/' + stock_symbol + '/financials'

    url_string = base_url + path
    return url_string


def get_balance_sheet_url(stock_symbol):
    """
    :param stock_symbol: e.g. 'nflx'
    :return: string representing url for balance seet
    e.g. 'https://www.nasdaq.com/symbol/nflx/financials?query=balance-sheet'
    """
    financials_url = get_income_url(stock_symbol)
    query = '?query=balance-sheet'
    url_string = financials_url + query
    return url_string


def get_html_from_web(stock_symbol):
    """
    Uses browser to request info.
    Waits for javascript to run and return html. Selects by css_id.
    :param url: url to load
    :param css_id: id of page html element to select
    return html. return empty string if timeout or error
    """

    browser = webdriver.Chrome()

    url = get_url(stock_symbol)
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


def get_dataframe_from_file(filename):
    """
    # reads data from local file. This can be handy during development.
    :param filename: e.g. './data/<stock_symbol>.html', './data/nflx.html'
    :return: a pandas dataframe
    """

    dataframes = pd.read_html(filename, header=0, index_col=0, skiprows=0)

    # read_html returns a list of dataframes, get the first one
    df = dataframes[0]

    df = cleaned_df(df)
    return df


def get_income_df_from_web(stock_symbol):
    """
    constructs a url from stock_symbol, downloads web page, returns dataframe
    :param stock_symbol: e.g. 'nflx'
    :return: a pandas dataframe containing income
    """

    url = get_income_url(stock_symbol)
    html = get_html_from_web(url)
    dataframes = pd.read_html(html, header=0, index_col=0, skiprows=0)

    # read_html returns a list of dataframes, get the first one
    df0 = dataframes[0]

    df_cleaned = cleaned_df(df0)
    return df_cleaned


def cleaned_df(df):
    """
    :param df: dataframe of the form returned by get_income_df_from_web or get_dataframe_from_file
    :return: dataframe with 4 columns containing amounts in thousands of dollars $000
    """
    # drop rows with all values NaN (Not A Number)
    df = df.dropna(how='all')

    # print(df.columns.values)
    # get desired column names. Note the dates may change over time.
    column_names = df.columns.values[1:5]
    # print(column_names)
    # ['12/31/2018' '12/31/2017' '12/31/2016' '12/31/2015']

    # the dollar amounts are in columns Unnamed:25 through Unnamed:28
    # slice to keep columns with dollar amounts
    df = df.loc[:, 'Unnamed: 25': 'Unnamed: 28']
    # re-add column names
    df.columns = column_names

    return df


def get_revenue(df):
    """
    :param df:
    :return: total revenue as a float
    """
    # pandas loc slice [:, 0:1] gets all rows, columns 0 through 1 inclusive
    newest_year_df = df.iloc[:, 0:1]
    revenue_dollar_string = newest_year_df.loc['Total Revenue', :].values[0]
    revenue = dollars(revenue_dollar_string)
    return revenue


# TODO: get dataframe containing equity
# def get_equity(df):
#     """
#     :param df: dataframe containing equity
#     :return: equity as a float
#     """
#     # pandas loc slice [:, 0:1] gets all rows, columns 0 through 1 inclusive
#     newest_year_df = df.iloc[:, 0:1]
#     equity_dollar_string = newest_year_df.loc['Equity', :].values[0]
#     equity = dollars(equity_dollar_string)
#     return equity


def dollars(dollar_string):
    """
    :param dollar_string: a string representing dollars () for negative amount e.g. $(100.21)
    :return: a float e.g. -100.21
    """

    if "(" in dollar_string:
        # prepend minus sign
        dollar_string = "-" + dollar_string

    # remove any parentheses
    dollar_string = dollar_string.replace('(', '')
    dollar_string = dollar_string.replace(')', '')

    # remove dollar sign
    dollar_string = dollar_string.replace('$', '')
    # remove comma
    dollar_string = dollar_string.replace(',', '')

    amount = float(dollar_string)
    return amount


if __name__ == '__main__':

    stock_symbol = 'nflx'

    filename = get_income_html_filename(stock_symbol)
    income_df = get_dataframe_from_file(filename)

    # alternatively
    # income_df = get_income_df_from_web(stock_symbol)

    print(income_df)

    # write income dataframe to a csv file
    # many programs can read this format e.g. pandas, excel
    income_df.to_csv('./data/' + stock_symbol + '_income.csv')

    revenue = get_revenue(income_df)
    print(revenue)
