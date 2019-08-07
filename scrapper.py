#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd
import filename_constructor
import url_constructor


"""
reference websearcher browser_driver.py
https://github.com/beepscore/websearcher
"""

# css id used to select html containing table within page html. Includes a little additional html
css_id = 'financials-iframe-wrap'
# use a separator other than ',' to ignore commas within amounts
separator = '|'


def get_html_from_web(url):
    """
    Uses browser to request info.
    Waits for javascript to run and return html. Selects by css_id.
    :param url: url to load
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


def get_dataframe_from_csv_file(filename):
    """
    # reads data from local file. This can be handy during development.
    :param filename: e.g. './data/<stock_symbol>_balance_sheet.csv', './data/nflx_balance_sheet.csv'
    :return: a pandas dataframe
    """

    df = pd.read_csv(filename, header=0, index_col=0, skiprows=0, sep=separator)
    return df


def get_dataframe_from_html_file(filename):
    """
    # reads data from local html file.
    This can be handy during development.
    For example you may load a web page and manually save the html into an .html file
    Then load .html file and adjust parsing/cleaning methods.
    After initial development, csv is a better format for use with Pandas.
    :param filename: e.g. './data/<stock_symbol>.html', './data/nflx.html'
    :return: a pandas dataframe
    """

    dataframes = pd.read_html(filename, header=0, index_col=0, skiprows=0)

    # read_html returns a list of dataframes, get the first one
    df = dataframes[0]

    df = cleaned_income_df(df)
    return df


def get_df_from_web(url):
    """
    constructs a url from stock_symbol, downloads web page, returns dataframe
    :param url: nasdaq url containing a stock symbol
    :return: a pandas dataframe
    """

    html = get_html_from_web(url)
    dataframes = pd.read_html(html, header=0, index_col=0, skiprows=0)

    # read_html returns a list of dataframes, get the first one
    df0 = dataframes[0]

    df_cleaned = cleaned_income_df(df0)
    return df_cleaned


def get_balance_sheet_df_from_web(stock_symbol):
    """
    constructs a url from stock_symbol, downloads web page, returns dataframe
    :param stock_symbol: e.g. 'nflx'
    :return: a pandas dataframe containing balance sheet
    """
    url = url_constructor.get_balance_sheet_url(stock_symbol)
    return get_df_from_web(url)


def get_income_df_from_web(stock_symbol):
    """
    constructs a url from stock_symbol, downloads web page, returns dataframe
    :param stock_symbol: e.g. 'nflx'
    :return: a pandas dataframe containing income
    """
    url = url_constructor.get_income_url(stock_symbol)
    return get_df_from_web(url)


def cleaned_income_df(df):
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


def get_net_income(df):
    """
    :param df: dataframe containing row with index 'Net Income'
    :return: total net_income as a Pandas series of float
    """
    net_income_series = df.loc['Net Income', :]
    # apply dollars() to convert string to float
    net_income_series = net_income_series.apply(dollars)
    return net_income_series


def get_revenue(df):
    """
    :param df: dataframe containing row with index 'Total Revenue'
    :return: total revenue as a Pandas series of float
    """
    revenue_series = df.loc['Total Revenue', :]
    # apply dollars() to convert string to float
    revenue_series = revenue_series.apply(dollars)
    return revenue_series


def get_equity(df):
    """
    :param df: dataframe containing row with index 'Total Equity'
    :return: equity as a Pandas series of float
    """
    equity_series = df.loc['Total Equity', :]
    # apply dollars() to convert string to float
    equity_series = equity_series.apply(dollars)
    return equity_series


def get_total_liabilities(df):
    """
    :param df: dataframe containing row with index 'Total Liabilities'
    :return: total liabilities as a Pandas series of float
    """
    total_liabilities_series = df.loc['Total Liabilities', :]
    # apply dollars() to convert string to float
    total_liabilities_series = total_liabilities_series.apply(dollars)
    return total_liabilities_series


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


def get_roic(income_df, balance_sheet_df):
    """
    :return: roic as a Pandas series of float
    """
    net_income_series = get_net_income(income_df)
    equity_series = get_equity(balance_sheet_df)
    total_liabilities_series = get_total_liabilities(balance_sheet_df)
    return net_income_series / (equity_series + total_liabilities_series)


if __name__ == '__main__':

    stock_symbol = 'nflx'

    # income_csv_filename = filename_constructor.get_income_csv_filename(stock_symbol)
    # income_html_filename = filename_constructor.get_income_html_filename(stock_symbol)
    # income_df = get_dataframe_from_html_file(income_html_filename)
    # alternatively
    # income_df = get_income_df_from_web(stock_symbol)
    # write dataframe to a csv file
    # income_df.to_csv(income_csv_filename, sep=separator)

    balance_sheet_csv_filename = filename_constructor.get_balance_sheet_csv_filename(stock_symbol)
    balance_sheet_df = get_dataframe_from_csv_file(balance_sheet_csv_filename)
    # alternatively
    # balance_sheet_df = get_balance_sheet_df_from_web(stock_symbol)
    # balance_sheet_df.to_csv(balance_sheet_csv_filename, sep=separator)

    # revenue = get_revenue(income_df)
    # print(revenue)

    equity = get_equity(balance_sheet_df)
