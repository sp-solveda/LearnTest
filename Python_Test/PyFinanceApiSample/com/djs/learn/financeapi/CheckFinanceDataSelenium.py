'''
Check finance data by Selenium.

Notes:
1. It requires 3rd parth python lib (at least): requests, selenium.
2. Selenium depends on:
   Firefox driver: https://github.com/mozilla/geckodriver/releases
   PhantomJS (Headless): http://phantomjs.org/download.html
3. Selenium 3.4.x and Geckodriver >=0.16.0 requires Firefox >=52.0.

Notes:
1. The page contents are generated by JavaScript, it cannot use Requests.

Update log: (date / version / author : comments)
2017-08-06 / 1.0.0 / Du Jiang : Creation
                                Support Firefox
                                Support Fundsupermart fund
2017-11-05 / 1.1.0 / Du Jiang : Support Google Finance stock
2017-11-07 / 1.3.0 / Du Jiang : Support Google Finance currency
2017-12-13 / 2.0.0 / Du Jiang : Support PhantomJS
                                Combined support Fundsupermart fund and Google Finance stock / currency.
2018-07-01 / 3.0.0 / Du Jiang : Remove Google Finance (Deprecated)
                                Support XE currency
'''

from concurrent.futures import ThreadPoolExecutor
import csv
import getopt
from http import HTTPStatus
import json
import sys
from time import localtime, strftime, sleep, time

import requests
from selenium import webdriver


# Global variables.
# The value can be updated by command line options.
__data_type = None
__inventory_info_file_path = None
__result_output_file_path = None
__concurrent_max_workers = 5
__web_driver_type = 0
__web_driver_file_path = None
__web_driver_log_file_path = None

__Constants = None


class Constants_Base(object):
    '''
    Use a class to keep constant variables.
    '''

    WAIT_PAGE_LOAD_MAX_TRY = 10
    # Seconds.
    WAIT_TIME_LOAD_PAGE = 3
    WAIT_TIME_VIEW_PAGE = 1

    RESULT = "Result"
    ERROR = "Error"

    RESULT_OK = "Ok"
    RESULT_ERROR = "Error"

    START_TIME = "Start time"
    STOP_TIME = "Stop time"

    INVENTORIES = "Inventories"
    RECORDS_NUMBER = "Records number"
    RECORD = "Record"
    INVENTORY_DATA = "Inventory data"

    URL = "URL"
    STATUS_CODE = "Status code"


class Constants_FundsupermartFund(Constants_Base):
    API_URL = "https://secure.fundsupermart.com/fsm/funds/factsheet/{0}/"

    FUND_NAME = "Fund name"
    FUND_ID = "Fund ID"

    SECTION_BANNER_INFO = "Banner info"
    SECTION_OFFER_TO_BID_INFO = "Offer to bid info"
    SECTION_BID_TO_OFFER_INFO = "Bid to offer info"
    SECTION_HISTORICAL_PRICE_INFO = "Historical price info"
    SECTION_RELEVANT_CHARGES = "Relevant charges"


class Constants_GoogleStock(Constants_Base):
    API_URL = "https://finance.google.com/finance?q={0}"

    COLUMN_NAME = "Name"
    COLUMN_EXCHANGE = "Exchange"
    COLUMN_TICKER = "Ticker"

    SECTION_STOCK_INFO = "Stock info"
    STOCK_INFO_NAME = "Name"
    STOCK_INFO_EXCHANGE = "Exchange"
    STOCK_INFO_TICKER = "Ticker"

    SECTION_MARKET_INFO = "Market info"
    MARKET_INFO_PRICE = "Price"
    MARKET_INFO_CURRENCY = "Currency"

    MARKET_INFO_52WEEK = "52 week"
    MARKET_INFO_52WEEK_LOW = "52 week low"
    MARKET_INFO_52WEEK_HIGH = "52 week high"

    MARKET_INFO_RANGE = "Range"
    MARKET_INFO_RANGE_LOW = "Range low"
    MARKET_INFO_RANGE_HIGH = "Range high"

    MARKET_INFO_DIVIDEND_YIELD = "Div/yield"
    MARKET_INFO_DIVIDEND = "Dividend"
    MARKET_INFO_YIELD = "Yield"

    MARKET_INFO_VOLUMES = "Vol / Avg."
    MARKET_INFO_AVG_VOLUME = "Avg. Volume"
    MARKET_INFO_VOLUME = "Volume"


class Constants_XeCurrency(Constants_Base):
    API_URL = "https://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}"

    COLUMN_NAME = "Name"
    COLUMN_FROM_SYMBOL = "From symbol"
    COLUMN_TO_SYMBOL = "To symbol"

    SECTION_CURRENCY_INFO = "Currency info"
    CURRENCY_INFO_FROM_SYMBOL = "From symbol"
    CURRENCY_INFO_TO_SYMBOL = "To symbol"

    SECTION_EXCHANGE_INFO = "Exchange info"
    EXCHANGE_INFO_VALUE = "Value"
    EXCHANGE_INFO_TIME = "Time"


def check_url(url):
    '''
    Use requests to get URL, and return HTTP status code.

    @param url: A string of URL.
    @return: HTTP response status code, or None if request failed.
    '''

    print("url =", url)
    status_code = None

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"}
        response = requests.get(url, headers=headers)
        # print("response =", response)
        print("response.status_code =", response.status_code)

        if response.history:
            status_code = HTTPStatus.OK
            print("response.status_code (Due to redirected) =", status_code)
        else:
            status_code = response.status_code
    except Exception as e:
        print("Check url: Exception = {0}".format(e))
        raise e

    return status_code


def check_page_loaded(browser):
    '''
    Check whether page is loaded.

    @param browser : Selenium handle.
    '''
    for i in range(0, __Constants.WAIT_PAGE_LOAD_MAX_TRY):
        # Wait for page to be fully loaded.
        sleep(__Constants.WAIT_TIME_LOAD_PAGE)
        try:
            if __data_type == 0:
                target_section = browser.find_element_by_id("factsheet")
            else:  # __data_type == 1:
                target_section = browser.find_element_by_class_name(
                    "converterresult-unitConversion")

            print("target_section =", target_section)

            if (target_section is None) or (not target_section):
                raise Exception("Not found target_section.")

            # It is ok, no need retry.
            break
        except Exception as e:
            print("Check page loaded: Count {0}: Exception = {1}".format(
                i, e))
            # browser.save_screenshot('screen' + str(i) + '.png')
            # If reach max try.
            if (i + 1) == __Constants.WAIT_PAGE_LOAD_MAX_TRY:
                raise e


def parse_get_data_fundsupoermart_fund(browser, results):
    '''
    Open URL and get data.

    @param browser : Selenium handle.
    @param results : Dict with return results.
    '''

    try:
        # Find links to sub-portals.

        try:
            factsheet_section = browser.find_element_by_id("factsheet")
            print("factsheet_section =", factsheet_section)
        except Exception:
            raise Exception("Cannot find factsheet_section.")
        results[__Constants.SECTION_BANNER_INFO] = {}

        try:
            treasure_overlay_spinner_section = factsheet_section.find_element_by_tag_name(
                "treasure-overlay-spinner")
            print("treasure_overlay_spinner_section =",
                  treasure_overlay_spinner_section)
        except Exception:
            raise Exception("Cannot find treasure_overlay_spinner_section.")

        try:
            banner_info_section = treasure_overlay_spinner_section.find_element_by_css_selector(
                "div[class='row m-t-md']")
            print("banner_info_section =", banner_info_section)
        except Exception:
            raise Exception("Cannot find banner_info_section.")

        try:
            element_sections = banner_info_section.find_elements_by_css_selector(
                "div[class*='col-md-3']")
            # print("element_sections =", element_sections)
        except Exception:
            raise Exception("Cannot find element_sections.")

        for element_section in element_sections:
            # print("element_section.text =", element_section.text)
            element_data = element_section.text.splitlines()
            print("element_data =", element_data)

            if len(element_data) > 1:
                if "Risk Rating" in element_data[1]:
                    item_data = element_data[1].split(":")
                    item_key = item_data[0].strip()
                    item_values = [item.strip()
                                   for item in item_data[1].split("-")]
                    results[__Constants.SECTION_BANNER_INFO][item_key] = item_values[0]
                    results[__Constants.SECTION_BANNER_INFO][item_key +
                                                             " Description"] = item_values[1]
                elif "NAV Price" in element_data[1]:
                    loc = element_data[1].find("(")
                    item_key = element_data[1][:loc].strip()
                    item_value = element_data[1][loc + 1:-1]
                    results[__Constants.SECTION_BANNER_INFO][item_key] = element_data[0]
                    results[__Constants.SECTION_BANNER_INFO][item_key +
                                                             " Date"] = item_value
                else:
                    results[__Constants.SECTION_BANNER_INFO][element_data[1]
                                                             ] = element_data[0]
            else:
                results[__Constants.SECTION_BANNER_INFO][element_data[0]
                                                         ] = ""

        results[__Constants.SECTION_OFFER_TO_BID_INFO] = {}

        try:
            offer_to_bid_info_section = factsheet_section.find_element_by_id(
                "offer-to-bid")
            print("offer_to_bid_info_section =", offer_to_bid_info_section)
        except Exception:
            raise Exception("Cannot find offer_to_bid_info_section.")

        try:
            list_section = offer_to_bid_info_section.find_element_by_css_selector(
                "div[class='tab-pane ng-scope active']")
        except Exception:
            raise Exception("Cannot find list_section.")

        try:
            element_sections = list_section.find_elements_by_tag_name(
                "li")
            # print("element_sections =", element_sections)
        except Exception:
            raise Exception("Cannot find element_sections.")

        for element_section in element_sections:
            # print("element_section.text =", element_section.text)
            element_data = element_section.text.splitlines()
            print("element_data =", element_data)
            results[__Constants.SECTION_OFFER_TO_BID_INFO][element_data[1]
                                                           ] = element_data[0]

        results[__Constants.SECTION_BID_TO_OFFER_INFO] = {}

        try:
            bid_to_offer_info_section = factsheet_section.find_element_by_id(
                "bid-to-return")
            print("bid_to_offer_info_section =", bid_to_offer_info_section)
        except Exception:
            raise Exception("Cannot find bid_to_offer_info_section.")

        try:
            list_section = bid_to_offer_info_section.find_element_by_css_selector(
                "div[class='tab-pane ng-scope active']")
        except Exception:
            raise Exception("Cannot find list_section.")

        try:
            element_sections = list_section.find_elements_by_tag_name(
                "li")
            # print("element_sections =", element_sections)
        except Exception:
            raise Exception("Cannot find element_sections.")

        for element_section in element_sections:
            # print("element_section.text =", element_section.text)
            element_data = element_section.text.splitlines()
            print("element_data =", element_data)
            results[__Constants.SECTION_BID_TO_OFFER_INFO][element_data[1]
                                                           ] = element_data[0]

        results[__Constants.SECTION_HISTORICAL_PRICE_INFO] = {}

        try:
            historical_price_info_section = factsheet_section.find_element_by_id(
                "fund-historical-price")
            print("historical_price_info_section =",
                  historical_price_info_section)
        except Exception:
            raise Exception("Cannot find historical_price_info_section.")

        try:
            list_section = historical_price_info_section.find_element_by_css_selector(
                "div[class='tab-pane ng-scope active']")
        except Exception:
            raise Exception("Cannot find list_section.")

        try:
            element_sections = list_section.find_elements_by_tag_name(
                "li")
            # print("element_sections =", element_sections)
        except Exception:
            raise Exception("Cannot find element_sections.")

        for element_section in element_sections:
            # print("element_section.text =", element_section.text)
            element_data = element_section.text.splitlines()
            print("element_data =", element_data)
            results[__Constants.SECTION_HISTORICAL_PRICE_INFO][element_data[1]
                                                               ] = element_data[0]

        results[__Constants.SECTION_RELEVANT_CHARGES] = {}

        try:
            relevant_charges_section = factsheet_section.find_element_by_id(
                "relevant-charges")
            print("relevant_charges_section =", relevant_charges_section)
        except Exception:
            raise Exception("Cannot find relevant_charges_section.")

        try:
            list_section = relevant_charges_section.find_element_by_css_selector(
                "div[class='m-t-xs']")
        except Exception:
            raise Exception("Cannot find list_section.")

        try:
            element_sections = list_section.find_elements_by_tag_name(
                "div")
            # print("element_sections =", element_sections)
        except Exception:
            raise Exception("Cannot find element_sections.")

        for element_section in element_sections:
            # print("element_section.text =", element_section.text)
            element_data = element_section.text.splitlines()
            print("element_data =", element_data)

            if "Expense Ratio" in element_data[1]:
                loc = element_data[1].find("(")
                item_key = element_data[1][:loc].strip()
                loc = element_data[1].find("of")
                item_value = element_data[1][loc + 3:-1]
                results[__Constants.SECTION_RELEVANT_CHARGES][item_key] = element_data[0]
                results[__Constants.SECTION_RELEVANT_CHARGES]["Annual Expense Ratio Date"] = item_value
            else:
                results[__Constants.SECTION_RELEVANT_CHARGES][element_data[1]
                                                              ] = element_data[0]

        print("Get fund data: ok.")
        print("-" * 40)
    except Exception as e:
        print("Get fund data: Exception = {0}".format(e))
        raise e


def parse_get_data_xe_currency(browser, results):
    '''
    Open URL and get data.

    @param browser : Selenium handle.
    @param results : Dict with return results.
    '''

    try:
        # ration section.

        try:
            ratio_section = browser.find_element_by_class_name(
                "converterresult-unitConversion")
            print("ratio_section =", ratio_section)
        except Exception:
            raise Exception("Cannot find ratio_section.")

        ratio = ratio_section.text.split()
        print("ratio =", ratio)

        results[__Constants.SECTION_CURRENCY_INFO] = {}
        results[__Constants.SECTION_EXCHANGE_INFO] = {}

        if len(ratio) == 5:
            results[__Constants.SECTION_CURRENCY_INFO][__Constants.CURRENCY_INFO_FROM_SYMBOL] = ratio[1]
            results[__Constants.SECTION_CURRENCY_INFO][__Constants.CURRENCY_INFO_TO_SYMBOL] = ratio[4]
            results[__Constants.SECTION_EXCHANGE_INFO][__Constants.EXCHANGE_INFO_VALUE] = ratio[3]

        try:
            time_section = browser.find_element_by_class_name("resultTime")
            print("time_section =", ratio_section)
            print("time =", time_section.text)
            results[__Constants.SECTION_EXCHANGE_INFO][__Constants.EXCHANGE_INFO_TIME] = time_section.text
        except Exception:
            pass

        print("Get currency data: ok.")
        print("-" * 40)
    except Exception as e:
        print("Get currency data: Exception = {0}".format(e))
        raise e


def inspect_inventory(record):
    '''
    Inspect inventory info page.

    @param record: [Fund name, Fund ID], [Stock name, Exchange, Ticker], [Currency from_symbol, To symbol] 
    @return : Dict with return results.
    '''

    results = {}

    if __data_type == 0:
        parse_get_data = parse_get_data_fundsupoermart_fund

        fund_name, fund_id = record
        fund_name = fund_name.strip()
        fund_id = fund_id.strip()
        print("fund_name =", fund_name)
        print("fund_id =", fund_id)
        inventory_id = fund_id

        results[inventory_id] = {}
        result = results[inventory_id]

        result[__Constants.RECORD] = {}
        result[__Constants.RECORD][__Constants.FUND_NAME] = fund_name
        result[__Constants.RECORD][__Constants.FUND_ID] = fund_id

        url = __Constants.API_URL.format(fund_id)
    else:  # __data_type == 1:
        parse_get_data = parse_get_data_xe_currency

        currency_info_from_symbol, currency_info_to_symbol = record
        currency_info_from_symbol = currency_info_from_symbol.strip()
        currency_info_to_symbol = currency_info_to_symbol.strip()
        print("currency_info_from_symbol =", currency_info_from_symbol)
        print("currency_info_to_symbol =", currency_info_to_symbol)
        inventory_id = currency_info_from_symbol + currency_info_to_symbol

        results[inventory_id] = {}
        result = results[inventory_id]

        result[__Constants.RECORD] = {}
        result[__Constants.RECORD][__Constants.COLUMN_FROM_SYMBOL] = currency_info_from_symbol
        result[__Constants.RECORD][__Constants.COLUMN_TO_SYMBOL] = currency_info_to_symbol

        url = __Constants.API_URL.format(
            currency_info_from_symbol, currency_info_to_symbol)

    print("url =", url)
    result[__Constants.URL] = url

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Start time =", time_str)
    result[__Constants.START_TIME] = time_str

    browser = None
    try:
        status_code = check_url(url)
        if status_code != HTTPStatus.OK:
            raise Exception("Get '{0}' failed with status code {1}.".format(url,
                                                                            status_code))

        if __web_driver_type == 0:  # PhantomJS.
            browser = webdriver.PhantomJS(
                executable_path=__web_driver_file_path, service_log_path=__web_driver_log_file_path)
        else:  # __web_driver_type == 1:  # FireFox.
            # Create profile.
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override",
                                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0")
            browser = webdriver.Firefox(
                profile, executable_path=__web_driver_file_path, log_path=__web_driver_log_file_path)

        print("browser =", browser)
        print("-" * 60)

        # Load page.
        browser.get(url)
        # Wait for page to be fully loaded.
        check_page_loaded(browser)
        print("-" * 40)

        # Parse and get data.
        result[__Constants.INVENTORY_DATA] = {}
        parse_get_data(browser, result[__Constants.INVENTORY_DATA])
        sleep(__Constants.WAIT_TIME_VIEW_PAGE)
        print("-" * 40)

        print("Inspect inventory <{0}>: ok.".format(inventory_id))
        result[__Constants.RESULT] = __Constants.RESULT_OK
    except Exception as e:
        print("Inspect inventory <{0}> Exception = {1}".format(
            inventory_id, e))
        result[__Constants.RESULT] = __Constants.RESULT_ERROR
        result[__Constants.ERROR] = repr(e)
    finally:
        if browser:
            print("Close browser.")
            browser.close()

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Stop time =", time_str)
    result[__Constants.STOP_TIME] = time_str

    return results


def process_inventory_list():
    '''
    Get a list of inventory info from a config file.
    Inspect each of them.

    @return: Dict with return results.
    '''

    global __Constants

    if __data_type == 0:
        __Constants = Constants_FundsupermartFund
    else:  # __data_type == 1:
        __Constants = Constants_XeCurrency

    results = {}

    print("-" * 100)
    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Start time =", time_str)
    results[__Constants.START_TIME] = time_str

    try:
        results[__Constants.INVENTORIES] = {}

        # Open input file.
        with open(__inventory_info_file_path) as record_file:
            print('record_file =', record_file)
            cin = csv.reader(record_file)
            # Get all records.
            records = [line for line in cin]
            # But not header line.
            records.pop(0)
            print("records =", records)
            results[__Constants.RECORDS_NUMBER] = len(records)
        print("-" * 80)

        # Inspect inventory concurrently.
        with ThreadPoolExecutor(max_workers=__concurrent_max_workers) as executor:
            # Wait for result to return.
            for record, result in zip(records, executor.map(inspect_inventory, records)):
                results[__Constants.INVENTORIES].update(result)

        print("-" * 80)
        print("Process inventory list: ok.")
    except Exception as e:
        print("Process inventory list: Exception = {0}".format(e))

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Stop time =", time_str)
    results[__Constants.STOP_TIME] = time_str

    print("Results =", results)
    print("-" * 100)

    # If given __result_output_file_path, output to file; otherwise, output to
    # screen.
    if __result_output_file_path:
        try:
            # Open output file.
            with open(__result_output_file_path, "w") as result_file:
                print('result_file =', result_file)
                # Output file as JSON format.
                json.dump(results, result_file, indent=4, sort_keys=True)
        except Exception as e:
            print("Output process results: Exception = {0}".format(e))
    else:
        # Output screen as JSON format.
        print(json.dumps(results, indent=4, sort_keys=True))

    print("-" * 100)

    return results


def usage():
    print('''
Check finance data by Selenium.

Usage:
-h
-d <DataType> -i <FilePath> [-o <FilePath>] [-c <Number>] [-t <DriverType>] -w <FilePath> [-l <FilePath>]

Options:
-h : Show help.
-d <DataType> : Finance data type. Compulsory, Value [0: Fundsupermart fund, 1: XE currency].
-i <FilePath> : Environment info file path (CSV). Compulsory.
-o <FilePath> : Result output file path (JSON). Optional, output to screen by default.
-c <Number> : Concurrent max workers to process records. Optional, Value [1, 10], 5 by default.
-t <DriverType> : Selenium web driver type. Optional, Value [0: PhantomJS, 1: Firefox], 0 by default.
-w <FilePath> : Selenium web driver file path (absolute path). For example, geckodriver for Firefox. Compulsory.
-l <FilePath> : Selenium web driver log file path. Optional, output to screen by default.

Notes:
Inventory info file format sample (With header line):
1. Fundsupermart fund
Fund name,Fund ID
2. XE currency
From symbol,To symbol

Notes:
1. It requires 3rd parth python lib (at least): requests, selenium.
2. Selenium depends on:
   PhantomJS (Headless): http://phantomjs.org/download.html
   Firefox driver: https://github.com/mozilla/geckodriver/releases
3. Selenium 3.4.x and Geckodriver >=0.16.0 requires Firefox >=52.0.
''')


def main(argv):
    '''
    Pass input arguments from command line to method.

    @param argv: A list of arguments
    '''

    global __data_type
    global __inventory_info_file_path
    global __result_output_file_path
    global __concurrent_max_workers
    global __web_driver_type
    global __web_driver_file_path
    global __web_driver_log_file_path

    print("argv =", argv)

    __show_usage = False
    __exit_code = 0
    __error_message = None

    # If no any option.
    if not argv:
        __show_usage = True

    # Parse command line.
    if not __show_usage:
        try:
            opts, args = getopt.getopt(argv, "hd:i:o:c:t:w:l:")
            print("opts =", opts)
            print("args =", args)
        except Exception as e:
            # There would be getopt.GetoptError.
            print("Parse command line: Exception = {0}".format(e))
            __show_usage, __exit_code, __error_message = True, -1, "Wrong command line option."

    # Check and parse each option.
    if not __show_usage:
        try:
            for opt, arg in opts:
                if opt == "-h":
                    __show_usage, __exit_code = True, 0
                elif opt == "-d":
                    __data_type = int(arg)
                elif opt == "-i":
                    __inventory_info_file_path = arg
                elif opt == "-o":
                    __result_output_file_path = arg
                elif opt == "-c":
                    __concurrent_max_workers = int(arg)
                elif opt == "-t":
                    __web_driver_type = int(arg)
                elif opt == "-w":
                    __web_driver_file_path = arg
                elif opt == "-l":
                    __web_driver_log_file_path = arg
                else:
                    __show_usage, __exit_code, __error_message = True, - \
                        2, "Unknown command line option."
        except Exception as e:
            print("Parse command options: Exception = {0}".format(e))
            __show_usage, __exit_code, __error_message = True, - \
                3, "Wrong value for command line option."

    print("show_usage =", __show_usage)
    print("data_type =", __data_type)
    print("inventory_info_file_path =", __inventory_info_file_path)
    print("result_output_file_path", __result_output_file_path)
    print("concurrent_max_workers =", __concurrent_max_workers)
    print("web_driver_type =", __web_driver_type)
    print("web_driver_file_path =", __web_driver_file_path)
    print("web_driver_log_file_path =", __web_driver_log_file_path)

    # Check options are valid.
    if not __show_usage:
        if (__data_type is None) or (__inventory_info_file_path is None) or (__web_driver_file_path is None):
            __show_usage, __exit_code, __error_message = True, - \
                4, "Missing compulsory command line option."
        elif (__data_type < 0) or (__data_type > 1):
            __show_usage, __exit_code, __error_message = True, -5, "Wrong value for -d."
        elif (__concurrent_max_workers < 1) or (__concurrent_max_workers > 10):
            __show_usage, __exit_code, __error_message = True, -6, "Wrong value for -c."
        elif (__web_driver_type < 0) or (__web_driver_type > 1):
            __show_usage, __exit_code, __error_message = True, -7, "Wrong value for -t."

    if not __show_usage:
        process_inventory_list()
    else:
        print("__exit_code =", __exit_code)
        if __error_message:
            print("__error_message =", __error_message)
        print("")
        usage()
        sys.exit(__exit_code)


if __name__ == '__main__':
    main(sys.argv[1:])
