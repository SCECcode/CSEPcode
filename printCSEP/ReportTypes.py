#
# Create itemized list of the various summary reports that it can print
#
# Current expectation is that all reports are chronological
# ALL - a line for each expected result with the status
# Found_data - details in csv format for each data type
# Errors - prints a line for each non-successfull expected result indicating status
# Counts - summary showing expected results and number in each category
# found = x
# data_not_found = y
# file_note_found = z
# dir_not_found = n
# initial = t
# expected_total,sum of all states
#
# Include this string version until standard names are established
#
report_names = "All,Success,Errors,Summary"