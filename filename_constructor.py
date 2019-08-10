#!/usr/bin/env python3
from pathlib import Path

# many programs can read and write csv format e.g. pandas, excel


def get_balance_sheet_csv_filename(stock_symbol) -> Path:
    """
    :param stock_symbol: used to construct the csv data filename, e.g. 'nflx'
    :return: string representing filename
    e.g. Path object ./data/<stock_symbol>.html, ./data/nflx_income.html
    """
    name = stock_symbol + '_balance_sheet.csv'
    path = Path('.').joinpath('data', name)
    return path


def get_income_csv_filename(stock_symbol) -> Path:
    """
    :param stock_symbol: used to construct the csv data filename, e.g. 'nflx'
    :return: string representing filename
    e.g. Path object ./data/<stock_symbol>_income.csv, ./data/nflx_income.html
    """
    path = Path('.').joinpath('data').joinpath(stock_symbol + '_income.csv')
    return path


def get_income_html_filename(stock_symbol) -> Path:
    """
    :param stock_symbol: used to construct the html data filename, e.g. 'nflx'
    :return: string representing filename
    e.g. Path object e.g. ./data/<stock_symbol>.html, ./data/nflx_income.html
    """
    path = Path('.').joinpath('data').joinpath(stock_symbol + '_income.html')
    return path

