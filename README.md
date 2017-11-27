##Overview of CSEP utility programs:

##Main objects:

##Forecast group: One or more forecast models using the same inputs and running for the same time period

##Forecast model: ETAS, STEP, and others

##test_name: N-test, R-Test

##Forecast result format:
ntest_format_1
start_time,end_time
file template

ntest_format_2
start_time,end_time
filename,
xml_tag

##scheduled_result
scheduled_result_datetime
found_result_datetime

##Basic Logic:
Make an assumption that the same results are expected for all models in a forecast group.
Then:

define a forecast group with one or more models under test, 
and one or more test types for each model

for each model in forecast group:
figure out the scheduled result times over the period of interest

For each model in forecast group:
for each scheduled_result:
forecast_result = find_forecast_results(model_name,test_name,duration,forecast_result)

##Report Logic
for each scheduled_result:
  if result.status = Found
  print result.data
 
## find_forecast_results
input scheduled result list:
input test_names # code must of a interpreter for that test type
input test_formats 

is expected result directory found?
are expected result files found?
are expected test results found in file?




