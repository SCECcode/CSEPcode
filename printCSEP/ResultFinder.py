import ResultStatus
import STEPResultFormats
import ETASResultFormats

def get_result_data(expected_result,
                    config,
                    model_name,
                    test_name,
                    result_datetime):

    """
    This is the intermediate method that figures out which get data method to call
    """
    if model_name == "STEP" and test_name == "N":
        expected_result = STEPResultFormats.find_step_ntest_result(config,expected_result,result_datetime)
    elif model_name == "ETAS" and test_name == "N":
        expected_result = ETASResultFormats.find_etas_ntest_result(config,expected_result,result_datetime)
    else:
        print "Unexpected method %s and test %s"%(model_name,test_name)
        expected_result.status = ResultStatus.PARSER_NOT_FOUND

    return expected_result
