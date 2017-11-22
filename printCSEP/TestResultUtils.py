#
# Utilities for use with printTestResult scripts
#
import os
import sys
import re
import datetime
from TestResult import TestResult

def ndays(start_day, start_month, start_year, end_day, end_month, end_year):
    """
    Utility to create an date enumeration used to create test date directories
    """
    start = datetime.datetime(start_year, start_month, start_day)
    end = datetime.datetime(end_year, end_month, end_day)
    step = datetime.timedelta(days=1)
    result = []
    while start < end:
        res = [start.day, start.month, start.year]
        result.append(res)
        start += step
    return result

def valid_date(datestring):
    """
    input: CSEP Directory Date Format: YYYY-MM-DD
    return: True if matches standard format. False if not.
    Currently this checks only the date format, but does not check that
    the found directory dates are within the forecast start and end dates.
    This improvement would make this method check that only directories
    found during the start and end dates would match.
    """
    try:
        mat=re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', datestring)
        #print mat
        if mat is not None:
            return True
    except ValueError:
        pass
    return False


def expected_forecast_dates(start_year,start_month,start_day,end_year,end_month,end_day):
    """
    input: expected_forecast_date_strings
    output: array of test dates in directory string format
    """
    res = ndays(start_day,start_month,start_year,
                end_day,end_month,end_year)

    #
    # results are list of elements:
    # [month,day,year]
    sorted_string_list = []
    for x in res:
        year_mo_dy = "%4d-%02d-%02d"%(x[2],x[1],x[0])
        sorted_string_list.append(year_mo_dy)
    return sorted_string_list
