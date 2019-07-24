
#!/usr/bin/env python3


#from io import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
#import pandas as pd


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

if __name__ == '__main__':

    stock_symbol = 'nflx'
    url = url(stock_symbol)
    print(url)

    data = get_text(url, 'left-column-div')
    print(data)




