import ResultStatus
import datetime

def find_etas_ntest_result(config,expected_result,result_datetime):
    #
    # This method needs to be updated to complete conversions of the starttime and endtime into
    # right format, and then making sure the date comparisons below work correctly
    #
    etas_ntest_format_1_starttime = config["STEP"]["etas_ntest_format_1_starttime"]
    etas_ntest_format_1_endtime = config["STEP"]["etas_ntest_format_1_endtime"]
    etas_ntest_format_2_starttime = config["STEP"]["etas_ntest_format_2_starttime"]
    etas_ntest_format_2_endtime = config["STEP"]["etas_ntest_format_2_endtime"]

    #
    # Create datetime object from datetime string
    #
    res = result_datetime.replace('"','').split("-")
    res_datetime = datetime.datetime(int(res[0]), int(res[1]), int(res[2]))
    #
    # split the datetime strings to create datetime object that we can use in comparisons
    #
    res = etas_ntest_format_1_starttime.replace('"','').split("-")
    report_start_datetime = datetime.datetime(int(res[0]), int(res[1]), int(res[2]))
    res = etas_ntest_format_1_endtime.replace('"','').split("-")
    report_end_datetime = datetime.datetime(int(res[0]),int(res[1]),int(res[2]))

    res2 = etas_ntest_format_2_starttime.replace('"','').split("-")
    report2_start_datetime = datetime.datetime(int(res2[0]), int(res2[1]), int(res2[2]))
    res2 = etas_ntest_format_2_endtime.replace('"','').split("-")
    report2_end_datetime = datetime.datetime(int(res2[0]),int(res2[1]),int(res2[2]))


    if res_datetime > report_start_datetime and res_datetime < report_end_datetime:
        expected_result = read_etas_ntest_format_1(config,expected_result)
    elif res_datetime > report2_start_datetime and res_datetime < report2_end_datetime:
        expected_result = read_etas_ntest_format_2(config,expected_result)
    else:
        expected_result.status = ResultStatus.PARSER_NOT_FOUND

    return expected_result

def read_etas_ntest_format_1(config,expected_result):
    print "etas_nest_format_1"
    expected_result.status = ResultStatus.DIR_NOT_FOUND
    return expected_result

def read_etas_ntest_format_2(config,expected_result):
    print "etas_ntest_format_2"
    expected_result.status = ResultStatus.DIR_NOT_FOUND
    return expected_result