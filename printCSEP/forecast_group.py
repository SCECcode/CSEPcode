#!/usr/bin/env python
'''
    File name: forecast_group.py
    Author: Phil Maechling
    Date created: 11/05/2017
    Date last modified: 11/05/2017

    This is the main program for the CSEP result processing scripts.

    Usage:
    $./forecast_group.py

    Inputs:
    Platform and report spectific inputs to program are defined in file: forecast_group_report.cfg
    This file contains specific configuration paramaters used to define the report
    of interest. A CSEP result report specification configuration file include:

        forecast_group_name: one_day_models
        model_names: ETAS,STEP
        test_names: N,T

        report_start_date: (start_year, start_month, start_day)
        report_end_date: (end_year,end_month, end_day)
        path_to_CSEP_results: /home/csep/operations/results


    Outputs:
        Report module gives various output formats
        including all,success,errors,summary counts
        CSEP Test results file in csv format
        Results are printed to stdout and can be collected gen_fg_reportgen_fg_report.py > results.csv

'''
import sys
import ConfigParser
import datetime
import findResultDateTimes
import TestResult
import ResultStatus
import OutputFormat
import ResultFinder
#
# Global Variables used
#
__version__ = "v17.11.25"

if __name__ == "__main__":
    #
    # Create empty array of test results that will be printed to create output report
    # This is current a daily forecast date, which for this forecast group is daily
    #

    result_datetime_list = []   # Array of dates in string format on which forecast results are expected
                                # This is assumed to be the same for all forecasts in the forecast group
                                # Currently, this only operates on interval of days. This is because the results
                                # are stored in YYYY-MM_DD format directories. Forecast groups with intervals
                                # other than one day will require review to support the calculation of the
                                # expected result datetime. Look to see if the directory names for hourly
                                # forecasts place results in directories with hour:min:sec names.

    #
    # A forecast group is a list of expected_results
    #
    fg_results = []

    #
    # Define User Inputs - Read from forecast_groupfg_report.cfg file
    #
    config = ConfigParser.SafeConfigParser()
    config.read("forecast_group_report.cfg")

    forecast_group_names = config.get("CSEP_FG_REPORT","forecast_group_names")
    forecast_group_name_list = forecast_group_names.replace('"','').split(",")
    #print "Number of forecast_groups:", len(forecast_group_name_list)

    model_names = config.get("CSEP_FG_REPORT","model_names")
    model_name_list = model_names.replace('"','').split(",")
    #print "Number of model_names", len(model_name_list)

    test_names = config.get("CSEP_FG_REPORT","test_names")
    test_name_list = test_names.replace('"','').split(",")
    #print "Number of tests",len(test_name_list)

    report_names = config.get("CSEP_FG_REPORT","report_names")
    report_name_list = report_names.replace('"','').split(",")
    #print "Number of reports",len(report_name_list)

    forecast_start_year = int(config.get("CSEP_FG_REPORT","forecast_start_year"))
    forecast_start_month = int(config.get("CSEP_FG_REPORT","forecast_start_month"))
    forecast_start_day = int(config.get("CSEP_FG_REPORT","forecast_start_day"))
    forecast_end_year = int(config.get("CSEP_FG_REPORT","forecast_end_year"))
    forecast_end_month = int(config.get("CSEP_FG_REPORT","forecast_end_month"))
    forecast_end_day = int(config.get("CSEP_FG_REPORT","forecast_end_day"))

    #
    # Convert the start and end times to datetimes
    #
    report_start_datetime = datetime.datetime(forecast_start_year, forecast_start_month, forecast_start_day)
    report_end_datetime = datetime.datetime(forecast_end_year, forecast_end_month, forecast_end_day)

    #
    # Create a list of expected test dates
    #
    #
    result_datetime_list = findResultDateTimes.expected_result_datetimes(report_start_datetime,
                                                                         report_end_datetime)

    #print "Expected Number of Forecast Results:",len(result_datetime_list)

    curdate = datetime.datetime.now()

    #
    # Look for each expected result in filesystem and
    # assign a status to each result for later reports.
    # This processes through the expected results, from oldest to latest
    # For each result, it checks each model, and for each model, it checks each test
    # when it gets to a specific expected result, it calls get_result_data to find
    # it on the filesystem. All successfully retrieved results are returned
    # in the TestResult object. This object also includes path to file
    # where the result was found.
    #
    for my_datetime in result_datetime_list:
        for my_forecast_group_name in forecast_group_name_list:
            for my_model_name in model_name_list:
                for my_test_name in test_name_list:
                    test_result = TestResult.TestResult()
                    test_result.forecast_group_name = my_forecast_group_name
                    test_result.status = ResultStatus.INITIAL
                    test_result.softwareVersion = __version__
                    test_result.test_name = my_test_name
                    test_result.model_name = my_model_name
                    test_result.resultDateTime = my_datetime
                    test_result.processingDateTime = "%4d-%02d-%02d"%(curdate.year, curdate.month, curdate.day)
                    test_result = ResultFinder.get_result_data(test_result,
                                                                config,
                                                                my_model_name,
                                                                my_test_name,
                                                                my_datetime)
                    fg_results.append(test_result)


    #
    # One or more reports can be generated about this format group using
    # configuration items in the forecast_group_report.cfg file
    #

    for report in report_name_list:
        OutputFormat.report(report,
                            fg_results,
                            report_start_datetime,
                            report_end_datetime)

    #
    # Exit Success
    #
    sys.exit(True)