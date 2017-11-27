#
# This contains utilities to convert the starttime endtime (and
# result_interval) into a series of result dates. These result dates
# are put into an array, and then processing is done for each expected
# result date. This may need to be generalized to calculated expected result datetimes that
# are not one-day-models, but are monthly, or hourly. This may involved introducing a interval
# variable into the calling parameters.
#
# Returns:
# the return format is an array of strings, in order, with the strings in this format: YYYY-MM-DD
#
#

import datetime

def ndays(start_datetime, end_datetime):
    """
    Utility to create an date enumeration used to create test date directories
    """
    start = start_datetime # datetime.datetime(start_year, start_month, start_day)
    end = end_datetime # datetime.datetime(end_year, end_month, end_day)
    step = datetime.timedelta(days=1)
    result = []
    while start < end:
        res = [start.day, start.month, start.year]
        result.append(res)
        start += step
    return result

def expected_result_datetimes(start_datetime,end_datetime):
    """
    input: expected_forecast_date_strings
    output: array of test dates in directory string format
    """
    res = ndays(start_datetime,end_datetime)

    #
    # results are list of elements:
    # [month,day,year]
    sorted_string_list = []
    for x in res:
        year_mo_dy = "%4d-%02d-%02d"%(x[2],x[1],x[0])
        sorted_string_list.append(year_mo_dy)
    return sorted_string_list