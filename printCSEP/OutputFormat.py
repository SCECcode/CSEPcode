import os
import ReportTypes
import datetime
import ResultStatus

def forecast_group_report_header(fg_results,report_start_datetime,report_end_datetime,modelnames,testnames):
    """
    print information common to the forecast group and the report
    """
    if len(fg_results) > 0:
        print "#forecastGroupName: %s" % (fg_results[0].forecast_group_name)
        print "#modelNames: %s" %(modelnames)
        print "#testNames: %s" % (testnames)
        print "#reportStartDate: %4d-%02d-%02d" % (report_start_datetime.year,
                                                    report_start_datetime.month,
                                                    report_start_datetime.day)
        print "#reportEndDate: %4d-%02d-%02d" % (report_end_datetime.year,
                                                    report_end_datetime.month,
                                                    report_end_datetime.day)
        print "#softwareVersion: %s" % (fg_results[0].softwareVersion)
        curdate = datetime.datetime.now()
        print "#currentDate: %4d-%02d-%02d" % (curdate.year, curdate.month, curdate.day)
        print "#number_of_expected_results: %d"%(len(fg_results))


def report(report_type,fg_results,report_start_datetime,report_end_datetime,modelnames,testnames):
    #
    # Currently defined reports in ReportTypes.py
    # report_names = "All,Success,Errors,Summary"
    #
    print "#------------- ReportType: %s -------------------"%(report_type)

    forecast_group_report_header(fg_results,
                                 report_start_datetime,
                                 report_end_datetime,
                                 modelnames,
                                 testnames)

    if report_type == "All":
        printAllRowStatus(fg_results)
    elif report_type == "Success":
        printFoundResults(fg_results)
    elif report_type == "Errors":
        print "print All Errors"
    elif report_type == "Summary":
        printSummaryCounts(fg_results)
    else:
        print "print Unknown report format:",report_type

def printSummaryCounts(fg_results):
    #
    # Iterate through results, count up each state of each expected result
    # print summary table
    #

    n_total_expected = len(fg_results)
    n_initial   = 0
    n_parser_not_found = 0
    n_dir_not_found = 0
    n_file_not_found = 0
    n_data_not_found = 0
    n_success = 0


    for result in fg_results:
        #print result.status
        if result.status == ResultStatus.INITIAL:
            n_initial += 1
        elif result.status == ResultStatus.PARSER_NOT_FOUND:
            n_parser_not_found += 1
        elif result.status == ResultStatus.DIR_NOT_FOUND:
            n_dir_not_found += 1
        elif result.status == ResultStatus.FILE_NOT_FOUND:
            n_file_not_found += 1
        elif result.status == ResultStatus.DATA_NOT_FOUND:
            n_data_not_found += 1
        elif result.status == ResultStatus.SUCCESS:
            n_success += 1
        else:
            print "Unknown Result State",result.status

    n_sum = n_initial + n_parser_not_found + \
            n_dir_not_found + n_file_not_found + \
            n_data_not_found + n_success

    print "#summary_of_expected_results: %d"%(n_total_expected)
    print "#Initial: %d"%(n_initial)
    print "#Parser Not Found: %d"%(n_parser_not_found)
    print "#Dir Not Found: %d"%(n_dir_not_found)
    print "#File Not Found: %d"%(n_file_not_found)
    print "#Data Not Found: %d"%(n_data_not_found)
    print "#Success: %d"%(n_success)
    print "#Total Expected Results: %d Sum Of Results: %d" % (n_total_expected,n_sum)


def printAllRowStatus(fg_results):
    for testResult in fg_results:
        """
        Pass in name of test: Eg. NTest
        prints only if one entry or more is in list
        Does a check to confirm
        """
        if testResult != None:
            print testResult # Use the intrinsic pring method.
        else:
            print "Found Null testResult:"


def printFoundResults(fg_results):

    good_results = 0
    for testResult in fg_results:
	if testResult.status == ResultStatus.SUCCESS:
		good_results += 1
    print "#number_of_found_results: %d"%(good_results)
    print "#resultDate,modelName,eventCount,delta1,delta2,eventCountForecast"
    for testResult in fg_results:
        if testResult.status == ResultStatus.SUCCESS:
            res = "%s," % (testResult.resultDateTime) + \
                "%s," % (testResult.model_name) + \
                "%10.8f," % (testResult.eventCount) + \
                "%10.8f," % (testResult.delta1) + \
                "%10.8f," % (testResult.delta2) + \
                "%10.8f" % (testResult.eventCountForecast)
            print res
