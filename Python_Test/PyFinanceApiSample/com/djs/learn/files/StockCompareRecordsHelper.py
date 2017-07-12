'''
Stock compare records helper.

Read records from a csv file. The file should have a header line.
Line format: Company name,Ticker,Selection date,Compare date

Update log: (date / version / author : comments)
2017-07-01 / 1.0.0 / Du Jiang : Creation
'''

from com.djs.learn.common import LoggingHelper
from com.djs.learn.common.CsvRecordsHelper import CsvRecordsHelper


FIELD_IDX_COMPANY_NAME = 0
FIELD_IDX_TICKER = 1
FIELD_IDX_SELECTION_DATE = 2
FIELD_IDX_COMPARE_DATE = 3


class StockCompareRecordsHelper(CsvRecordsHelper):
    '''
    Manage host records.
    '''

    __logger = LoggingHelper.get_logger("StockCompareRecordsHelper")

    def __init__(self, csv_filename):
        '''
        @param csv_filename: CSV file.
        '''
        super().__init__(csv_filename)

        self.__logger = StockCompareRecordsHelper.__logger
        self.__logger.debug("locals() = %s", locals())

    def find_by_ticker(self, ticker):
        '''
        Find record by ticker.

        @param ticker
        @return: Record, or None if not found.
        '''
        record = None

        # If hosts list is not empty.
        if self._records:
            # Check each item, and find matching one.
            for item in self._records:
                if self._use_dict:
                    if item[self._hearders[FIELD_IDX_TICKER]] == ticker:
                        record = item
                        break
                else:
                    if item[FIELD_IDX_TICKER] == ticker:
                        record = item
                        break
        return record