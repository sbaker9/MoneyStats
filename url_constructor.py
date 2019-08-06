#!/usr/bin/env python3


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

