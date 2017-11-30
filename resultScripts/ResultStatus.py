#
# Expected Forecast Evaluation Result Status
#
# Keep track of basic information about each expected result
# Currently Status Definitions include:
# SUCCESS = the forecast result was successfully read from a file
# DATA_NOT_FOUND = the forecast result was not found in the file
# FILE_NOT_FOUND = the forecast result file was not found
# DIR_NOT_FOUND = the forecast result directory was not found
# INITIAL = no processing of expected forecasts


INITIAL = "INITIAL"
PARSER_NOT_FOUND = "PARSER_NOT_FOUND"
DIR_NOT_FOUND = "DIR_NOT_FOUND"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
DATA_NOT_FOUND = "DATA_NOT_FOUND"
SUCCESS= "SUCCESS"