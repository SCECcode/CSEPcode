import ResultStatus
import Constants
import ResultFinder
class TestResult(object):
    """
    Define TestResult object.
    This object should support multiple result types including
    different test_types and different model_types
    """


    #
    # Initial new TestResult Objects with null strings
    # and invalid default data values for floats
    #
    def __init__(self):
        #
        # Status Info about the object inputs and parsed results
        #
        self.status = ResultStatus.INITIAL
        self.softwareVersion =  ""
        self.forecast_group_name = ""
        self.test_name = ""
        self.model_name = ""
        self.test_result_file_path = ""
        self.test_result_file_name = ""
        self.list_of_testfile_matches = []
        self.number_of_testfile_matches = 0
        self.resultDateTime = ""
        self.processingDateTime = ""
        #
        # These values are the eventual payload that we retrieve from the
        # current models under test
        #
        self.eventCount = Constants.default_invalid_data_value
        self.eventCountForecast = Constants.default_invalid_data_value
        self.delta1 = Constants.default_invalid_data_value
        self.delta2 = Constants.default_invalid_data_value


    def get_result_data(self,config,expected_result):
        expected_result = ResultFinder(expected_result,
                                       config)
        return expected_result


    #
    # Define method the prints these objects as a string.
    #
    def __str__(self):
        res = "\nresultStatus: %s\n"%(self.status) + \
            "softwareVesion: %s\n"%(self.softwareVersion) + \
            "processingDate: %s\n"%(self.processingDateTime) + \
            "forecast_group_name: %s\n"%(self.forecast_group_name) + \
            "model_name: %s\n"%(self.model_name) + \
            "test_name: %s\n"%(self.test_name) + \
            "test_result_file_path: %s\n"%(self.test_result_file_path) + \
            "test_result_file_name: %s\n"%(self.test_result_file_name) + \
            "num_of_resultfile_matches: %d\n"% (len(self.list_of_testfile_matches)) + \
            "eventCount: %f\n"%(self.eventCount) + \
            "delta1: %f\n"%(self.delta1) + \
            "delta2: %f\n"%(self. delta2) + \
            "eventCountForecast: %f\n"%(self.eventCountForecast) + \
            "resultDateTime: %s\n"%(self.resultDateTime)

        return res



#"number_of_testfile_matches: %s\n"(self.number_of_testfile_matches) + \