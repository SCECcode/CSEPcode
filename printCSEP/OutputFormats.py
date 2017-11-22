import os
def writeCVSHeader(test_date_list,test_result_list):
    """
    print constant header info from first entry in list
    """
    count_oks = 0
    for x in test_result_list:
        if x.status == x.RESFILE_OK:
            count_oks += 1

    if len(test_result_list) > 0:
        # remove date from first data directory
        res_dir = os.path.split(test_result_list[0].test_result_file_path)

        res = "#result_dir: %s\n"%(res_dir[0]) + \
              "#number_of_expected_results: %d\n"%(len(test_date_list)) + \
            "#number_of_found_results: %d\n"%(count_oks) + \
            "resultDate,modelName,eventCount,delta1,delta2,eventCountForecast" \
            ""
        print res

def writeCSVRow(testResult):
    """
    Pass in name of test: Eg. NTest
    prints only if one entry or more is in list
    Does a check to confirm
    """
    if testResult != None:
        res = "%s," % (testResult.testDate) + \
            "%s," % (testResult.modelname) + \
            "%10.8f," % (testResult.eventCount) + \
            "%10.8f," % (testResult.delta1) + \
            "%10.8f," % (testResult.delta2) + \
            "%10.8f" % (testResult.eventCountForecast)
        print res