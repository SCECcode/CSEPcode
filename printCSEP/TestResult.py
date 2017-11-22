class TestResult(object):
    """
    Define TestResult constants
    """

    #
    # Define a series of processing states
    # that the program goes through when locating results
    # for a given time period.
    #
    SCHEDULED = "Test Scheduled"
    RESDIR_FOUND = "Result Directory Found"
    RESDIR_NOTFOUND = "No Result Directory Found"
    RESFILE_FOUND = "Result File Found"
    RESFILE_NOTFOUND = "No Result File Found"
    RESFILE_OK = "Result File Ok"
    RESFILE_ERROR = "Result File Error"

    #
    # Define a single default value for all float
    # numbers. Strings default to empty string
    #
    default_invalid_data_value = -99999.0

    #
    # Initial new TestResult Objects with null strings
    # and invalid default data values for floats
    #
    def __init__(self):
        #
        # Status Info about the object inputs and parsed results
        #
        self.status = ""
        self.result_file_template = ""
        self.list_of_testfile_matches = []
        self.testresult_params = 0
        self.number_of_matching_files = 0
        #
        # Parsed Info with default values
        #
        self.test_result_file_path = ""
        self.test_result_file_name = ""
        self.modelname = ""
        self.eventCount = self.default_invalid_data_value
        self.delta1 = self.default_invalid_data_value
        self.delta2 = self.default_invalid_data_value
        self.eventCountForecast = self.default_invalid_data_value
        self.testDate = ""
        #
        # Currently Not Used
        #
        self.td_CSEPVersion =  ""
        self.td_creationTime = ""
        self.td_forecastEndDate = ""
        self.td_forecastStartDate = ""

    #
    # Define method the prints these objects as a string.
    #
    def __str__(self):
        res = "\nresultStatus: %s\n"%(self.status) + \
            "resultTemplate: %s\n"%(self.result_file_template) +\
             "test_file_path: %s\n"%(self.test_result_file_path) + \
            "test_result_file_name: %s\n"%(self.test_result_file_name) + \
            "modelname: %s\n"%(self.modelname) + \
            "eventCount: %f\n"%(self.eventCount) + \
            "delta1: %f\n"%(self.delta1) + \
            "delta2: %f\n"%(self. delta2) + \
            "eventCountForecast: %f\n"%(self.eventCountForecast) + \
            "testDate: %s\n"%(self.testDate)
        return res