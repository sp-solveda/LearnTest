'''
Check Fundsupermart fund data.

Update log: (date / version / author : comments)
2017-08-06 / 1.0.0 / Du Jiang : Creation

Note that:
1. This version ONLY supports FireFox.
2. It requires 3rd parth python lib (at least): requests, selenium.
3. Selenium depends on Geckodriver for Firefox.
   Download: https://github.com/mozilla/geckodriver/releases
4. Selenium 3.4.x and Geckodriver >=0.16.0 requires Firefox >=52.0.
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
from selenium.webdriver.common.keys import Keys


# Global variables.
# The value can be updated by command line options.
__geckodriver_file_path = None
__geckodriver_log_file_path = None
__fund_info_file_path = None
__result_output_file_path = None
__concurrent_max_workers = 5


class Constants(object):
    '''
    Use a class to keep constant variables.
    '''

    # Seconds.
    WAIT_TIME_LOAD_PAGE = 10
    WAIT_TIME_LOGIN_AND_LOAD = 20
    WAIT_TIME_LOAD_TAB = 10
    WAIT_TIME_QUICK_LOAD = 5
    WAIT_TIME_VERY_QUICK_LOAD = 2
    WAIT_TIME_FRESH_CONTENT = 5
    WAIT_TIME_VIEW_PAGE = 5

    RESULT = "Result"
    ERROR = "Error"

    RESULT_OK = "Ok"
    RESULT_ERROR = "Error"

    RECORDS = "Records"
    RECORD = "Record"

    START_TIME = "Start time"
    STOP_TIME = "Stop time"

    FUND_NAME = "Fund name"
    FUND_ID = "Fund ID"

    URL = "URL"
    STATUS_CODE = "Status code"

    FUND_DATA = "Fund data"


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
        status_code = response.status_code
    except Exception as e:
        print("Check url: Exception = {0}".format(e))
        raise e

    return status_code


def get_fund_data(browser, results):
    '''
    Open URL and get data

    @param browser : Selenium handle.
    @param results : Dict with return results.
    '''

    try:
        # Find links to sub-portals.
        factsheet_section = browser.find_element_by_id("factsheet")

        if factsheet_section:
            print("factsheet_section =", factsheet_section)

            treasure_overlay_spinner_section = factsheet_section.find_element_by_tag_name(
                "treasure-overlay-spinner")
            if treasure_overlay_spinner_section:
                print("treasure_overlay_spinner_section =",
                      treasure_overlay_spinner_section)
                banner_info_section = treasure_overlay_spinner_section.find_element_by_css_selector(
                    "div[class='row m-t-md']")
                if banner_info_section:
                    print("banner_info_section =", banner_info_section)
                    element_sections = banner_info_section.find_elements_by_css_selector(
                        "div[class*='col-md-3']")
                    if element_sections:
                        # print("element_sections =", element_sections)
                        for element_section in element_sections:
                            print("element_section.text =",
                                  element_section.text)

            offer_to_bid_info_section = factsheet_section.find_element_by_id(
                "offer-to-bid")
            if offer_to_bid_info_section:
                print("offer_to_bid_info_section =", offer_to_bid_info_section)
                list_section = offer_to_bid_info_section.find_element_by_css_selector(
                    "div[class='tab-pane ng-scope active']")
                if list_section:
                    element_sections = list_section.find_elements_by_tag_name(
                        "li")
                    if element_sections:
                        # print("element_sections =", element_sections)
                        for element_section in element_sections:
                            print("element_section.text =",
                                  element_section.text)

            bid_to_offer_info_section = factsheet_section.find_element_by_id(
                "bid-to-return")
            if bid_to_offer_info_section:
                print("bid_to_offer_info_section =", bid_to_offer_info_section)
                list_section = bid_to_offer_info_section.find_element_by_css_selector(
                    "div[class='tab-pane ng-scope active']")
                if list_section:
                    element_sections = list_section.find_elements_by_tag_name(
                        "li")
                    if element_sections:
                        # print("element_sections =", element_sections)
                        for element_section in element_sections:
                            print("element_section.text =",
                                  element_section.text)

            relevant_charges_section = factsheet_section.find_element_by_id(
                "relevant-charges")
            if relevant_charges_section:
                print("relevant_charges_section =", relevant_charges_section)
                list_section = relevant_charges_section.find_element_by_css_selector(
                    "div[class='m-t-xs']")
                if list_section:
                    element_sections = list_section.find_elements_by_tag_name(
                        "div")
                    if element_sections:
                        # print("element_sections =", element_sections)
                        for element_section in element_sections:
                            print("element_section.text =",
                                  element_section.text)
        else:
            raise Exception("Cannot find factsheet section.")

        print("Get fund data: ok.")
        print("-" * 40)
    except Exception as e:
        print("Get fund data: Exception = {0}".format(e))
        raise e


def inspect_fund(record):
    '''
    Inspect fund info page.

    @param record: [fund name, fund id] 
    @return : Dict with return results.
    '''

    global __geckodriver_file_path
    global __geckodriver_log_file_path

    results = {}

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Start time =", time_str)
    results[Constants.START_TIME] = time_str

    fund_name, fund_id = record
    print("fund_name =", fund_name)
    print("fund_id =", fund_id)

    results[Constants.RECORD] = {}
    results[Constants.RECORD][Constants.FUND_NAME] = fund_name
    results[Constants.RECORD][Constants.FUND_ID] = fund_id

    browser = None
    try:
        url = "https://secure.fundsupermart.com/fsm/funds/factsheet/{0}".format(
            fund_id)
        print("url =", url)
        results[Constants.URL] = url

        status_code = check_url(url)
        if status_code == HTTPStatus.OK:
            # Create profile.
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override",
                                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0")
            browser = webdriver.Firefox(
                profile, executable_path=__geckodriver_file_path, log_path=__geckodriver_log_file_path)
            print("browser =", browser)
            print("-" * 60)

            # Load page.
            browser.get(url)
            # Wait for page to be fully loaded.
            sleep(Constants.WAIT_TIME_LOAD_PAGE)
            print("-" * 40)

            # Get fund data.
            results[Constants.FUND_DATA] = {}
            get_fund_data(browser, results[Constants.FUND_DATA])
            sleep(Constants.WAIT_TIME_VIEW_PAGE)
            print("-" * 40)
        else:
            raise Exception("Get '{0}' failed with status code {1}.".format(url,
                                                                            status_code))

        print("Inspect fund: <{0}> ok.".format(fund_id))
        results[Constants.RESULT] = Constants.RESULT_OK
    except Exception as e:
        print("Inspect fund: <{0}> Exception = {1}".format(fund_id, e))
        results[Constants.RESULT] = Constants.RESULT_ERROR
        results[Constants.ERROR] = repr(e)
    finally:
        if browser:
            sleep(Constants.WAIT_TIME_VIEW_PAGE)
            print("Close browser.")
            browser.close()

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Stop time =", time_str)
    results[Constants.STOP_TIME] = time_str

    return results


def process_fund_list():
    '''
    Get a list of fund info from a config file.
    Inspect each of them.

    @return: Dict with return results.
    '''

    global __concurrent_max_workers
    global __fund_info_file_path
    global __result_output_file_path

    results = {}

    print("-" * 100)
    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Start time =", time_str)
    results[Constants.START_TIME] = time_str

    try:
        # Open input file.
        with open(__fund_info_file_path) as record_file:
            print('record_file =', record_file)
            cin = csv.reader(record_file)
            # Get all records.
            records = [line for line in cin]
            # But not header line.
            records.pop(0)
            print("records =", records)
            results[Constants.RECORDS] = len(records)
        print("-" * 80)

        # Inspect each env concurrently.
        with ThreadPoolExecutor(max_workers=__concurrent_max_workers) as executor:
            # Wait for result to return.
            for record, result in zip(records, executor.map(inspect_fund, records)):
                gtsonsl = record[0]
                results[gtsonsl] = result

        print("-" * 80)
        print("Process env list: ok.")
    except Exception as e:
        print("Process env list: Exception = {0}".format(e))

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
    print("Stop time =", time_str)
    results[Constants.STOP_TIME] = time_str

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
Check Fundsupermart fund data.

Usage:
-h
-i <file path> [-o <file path>] -w <file path>

Options:
-h : Show help.
-i <file path> : Environment info file path (CSV). Compulsory.
-o <file path> : Result output file path (JSON). Optional, output to screen by default.
-w <file path> : Selenium web driver file path. For example, geckodriver for Firefox. Compulsory.
-l <file path> : Selenium web driver log file path. Optional, output to screen by default.
-c : Concurrent max workers to process records. Optional, 5 by default. Must >= 1.

Fund info file format sample (With header line):
Fund name,Fund ID

Note that:
1. This version ONLY supports FireFox.
2. It requires 3rd parth python lib (at least): requests, selenium.
3. Selenium depends on Geckodriver for Firefox.
   Download: https://github.com/mozilla/geckodriver/releases
4. Selenium 3.4.x and Geckodriver >=0.16.0 requires Firefox >=52.0.
''')


def main(argv):
    '''
    Pass input arguments from command line to method.

    @param argv: A list of arguments
    '''

    global __geckodriver_file_path
    global __geckodriver_log_file_path
    global __fund_info_file_path
    global __result_output_file_path
    global __concurrent_max_workers

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
            opts, args = getopt.getopt(argv, "hi:o:w:l:c:")
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
                elif opt == "-i":
                    __fund_info_file_path = arg
                elif opt == "-o":
                    __result_output_file_path = arg
                elif opt == "-w":
                    __geckodriver_file_path = arg
                elif opt == "-l":
                    __geckodriver_log_file_path = arg
                elif opt == "-c":
                    __concurrent_max_workers = int(arg)
                else:
                    __show_usage, __exit_code, __error_message = True, - \
                        2, "Unknown command line option."
        except Exception as e:
            print("Parse command options: Exception = {0}".format(e))
            __show_usage, __exit_code, __error_message = True, - \
                3, "Wrong value for command line option."

    print("show_usage =", __show_usage)
    print("geckodriver_file_path =", __geckodriver_file_path)
    print("geckodriver_log_file_path =", __geckodriver_log_file_path)
    print("env_info_file_path =", __fund_info_file_path)
    print("result_output_file_path", __result_output_file_path)
    print("concurrent_max_workers =", __concurrent_max_workers)

    # Check options are valid.
    if not __show_usage:
        if (not __fund_info_file_path) or (not __geckodriver_file_path):
            __show_usage, __exit_code, __error_message = True, - \
                4, "Missing compulsory command line option."
        elif __concurrent_max_workers < 1:
            __show_usage, __exit_code, __error_message = True, -5, "Wrong value for -c."

    if not __show_usage:
        process_fund_list()
    else:
        print("__exit_code =", __exit_code)
        if __error_message:
            print("__error_message =", __error_message)
        print("")
        usage()
        sys.exit(__exit_code)


if __name__ == '__main__':
    main(sys.argv[1:])
