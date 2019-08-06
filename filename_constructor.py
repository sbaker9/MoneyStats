#!/usr/bin/env python3


# many programs can read and write csv format e.g. pandas, excel

def get_balance_sheet_csv_filename(stock_symbol):
    """
    :param stock_symbol: used to construct the csv data filename, e.g. 'nflx'
    :return: string representing filename
    e.g. './data/<stock_symbol>.html', './data/nflx_income.html'
    """
    path = './data/' + stock_symbol + '_balance_sheet.csv'
    return path


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


def get_income_csv_filename(stock_symbol):
    """
    :param stock_symbol: used to construct the csv data filename, e.g. 'nflx'
    :return: string representing filename
    e.g. './data/<stock_symbol>_income.csv', './data/nflx_income.html'
    """
    path = './data/' + stock_symbol + '_income.csv'
    return path


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


