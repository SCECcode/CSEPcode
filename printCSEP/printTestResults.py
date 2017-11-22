#!/usr/bin/env python
'''
    File name: printTestResults.py
    Author: Phil Maechling
    Date created: 11/05/2017
    Date last modified: 11/05/2017

    Inputs: CSEP Test results directory
            Test Name: (eg. NTest)
            start_date: (start_year, start_month, start_day)
            end_date: (end_year,end_month, end_day)


    -sy : start year (int)
    -sm : start month (int)
    -sd : start day (int)
    -ey: end year (int)
    -em : end month (int)
    -ed : end day (int)
    -rd : results_directory (string)
    -txt: test xml tag (string) (e.g NTEST)
    -trf : test result filestring (string)
            (e.g. N-Test is used in the filename for the summary N-Test result files)
    -rt : report_type (forecast_timeseries,
                        missing_directories
                        missing_result_files

    Outputs: CSEP Test results file in csv format
        Results are printed to stdout and can be collected printTestResults.py > results.csv

'''
import sys
from TestResult import TestResult
import TestResultUtils
import OutputFormats
import NTestFormats
import NTestFileFinder
import datetime
import configparser

#
# Global Variables used
#
__version__ = "v17.11.22"

if __name__ == "__main__":
    #
    # Create empty array of test results that will be printed to create output report
    #

    test_date_list = [] # Array of test_dates in string format
    test_result_list = [] # Arrray of testresult objects, used to generate reports

    #
    # Define User Inputs - Read from csep_results.cfg file
    #
    config = configparser.ConfigParser()
    config.read("csep_results.cfg")
    result_file_dir = config["DEFAULT"]["result_file_dir"]
    result_file_dir = result_file_dir.replace('"','') # remove any quote marks from string
    test_xml_name = config["DEFAULT"]["test_xml_name"]
    test_xml_name = test_xml_name.replace('"','') # remove any quote marks from string
    test_result_name = config["DEFAULT"]["test_result_name"]
    test_result_name = test_result_name.replace('"','') # remove any quote marks from string
    forecast_start_year = int(config["DEFAULT"]["forecast_start_year"])
    forecast_start_month = int(config["DEFAULT"]["forecast_start_month"])
    forecast_start_day = int(config["DEFAULT"]["forecast_start_day"])
    forecast_end_year = int(config["DEFAULT"]["forecast_end_year"])
    forecast_end_month = int(config["DEFAULT"]["forecast_end_month"])
    forecast_end_day = int(config["DEFAULT"]["forecast_end_day"])

    #
    # Create a list of expected test dates
    #
    #
    test_date_list = TestResultUtils.expected_forecast_dates(forecast_start_year,
                                                             forecast_start_month,
                                                              forecast_start_day,
                                                              forecast_end_year,
                                                              forecast_end_month,
                                                              forecast_end_day)
    #print "Expected Number of Forecast Results:",len(test_date_list)

    #
    # Create an list of TestResult Objects, and set their value:
    # Set the state to state1 = scheduled
    #
    test_result_list = []
    for days in test_date_list:
        tr = TestResult()
        tr.testDate = days
        tr.status = tr.SCHEDULED
        test_result_list.append(tr)

    #
    # Construct a path to the results directory, and check each scheduled testdate
    # for a results directory
    #
    test_result_list = NTestFileFinder.find_testresult_dirs(test_result_list,result_file_dir)

    #
    # Report on testdates with directories
    #
    for x in test_result_list:
        if x.status == x.RESDIR_FOUND:
            #print x.status, x.testDate,x.test_result_file_path
            pass
        else:
            pass

    #
    # Call routines to find and parse the test_result file
    #
    test_result_list = NTestFileFinder.find_testresult_files(test_result_list,test_result_name)

    #
    # Report on testdate files
    for x in test_result_list:
        if x.status == x.RESFILE_FOUND:
            pass
            #print x.testDate,x.status,x.test_result_file_name
        else:
            pass

    #
    # Call routines to find and parse the test_result file
    #
    test_result_list = NTestFormats.parse_testresult_files(test_result_list,test_xml_name)
    for x in test_result_list:
        if x.status == x.RESFILE_OK:
            pass
            #print "Good files:",x.testDate,x.test_result_file_name
        else:
            pass

    #
    # Print formatted csv to stdout. User must capture with redirect > outfile.csv
    # One row per model per day
    # Include header in output format with metadata
    #
    if len(test_result_list) > 0:
        #
        # Write file comment metadata header
        # Then write column headers
        # and write number of entries
        # Then write one row per forecast_per_day per test

        print "#testName: %s"%(test_xml_name)
        print "#startDate: %s"%(test_date_list[0])
        print "#endDate: %s"%(test_date_list[-1])
        print "#Script Version: %s"%(__version__)
        curdate = datetime.datetime.now()
        print "#CurrentDate: %4d-%02d-%02d"%(curdate.year,curdate.month,curdate.day)
        OutputFormats.writeCVSHeader(test_date_list,test_result_list)
        for x in test_result_list:
            if x.status == x.RESFILE_OK:
                OutputFormats.writeCSVRow(x)

    #
    #
    # Uncomment (change to True) and this will print a
    # list of missing directories for the full test period
    #
    if False:
        for x in test_result_list:
            if x.status == x.RESFILE_OK:
                print "Result file OK:",x.testDate,x.status,x.result_file_template
            elif x.status == x.RESFILE_ERROR:
                print "Result file error:",x.testDate,x.status,x.test_result_file_name
            elif x.status == x.RESFILE_NOTFOUND:
                print "Result file not found:",x.testDate,x.test_result_file_name
            elif x.status == x.RESDIR_NOTFOUND:
                print "Result directory not found:", x.testDate,x.test_result_file_path
            elif x.status == x.RESDIR_FOUND:
                print "Result directory found:", x.testDate,x.test_result_path_name
            elif x.status == x.SCHEDULED:
                print "Result scheduled:", x.testDate
            else:
                print "Unexpected result file state",x.status
    #
    # Exit Success
    #
    sys.exit(True)
