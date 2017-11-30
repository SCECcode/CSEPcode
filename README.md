## Overview of CSEP utility programs:
This SCEC CSEP software repository is for utility programs written to support CSEP science activities including analysis of results.

## Main Program Concepts:
The resultScript directory contains scripts for processing CSEP forecast evalation results.
The top level script is: $run_forecast_report.py

Before running the top level script, define the forecast_group_report that you want to generate.
Edit the forecast_group_report.cfg file with a text editor.

Define the forecast group of interest, the forecast models (e.g. STEP, ETAS), and the evalation tests (N,T), and
a start_date and end_date. Reports can include all found data, missing data, or a combination of both.

# Forecast group: One or more forecast models using the same inputs and running for the same time period
# Forecast model: ETAS, STEP, and others
# test_name: N-test, R-Test

## Basic Logic:
If the same output reports are expected for all models in a forecast group.
Then:

define a forecast group with one or more models under test, 
and one or more test types for each model

for each model in forecast group:
figure out the scheduled result times over the period of interest

For each model in forecast group:
for each scheduled_result:
forecast_result = find_forecast_results(model_name,test_name,duration,forecast_result)

## Basic Report Logic
for each scheduled_result:
  if result.status = SUCCESS
       print result.data
 
## Adding a new Model or Test
The program will call get_result_data() for every result
and ther current codes figures out which subroutine to call
to parse that model or test result.

The source files affected if you add a new model or test include:

#ResultFinder

This method tests for each combination of model and test and calls
the correct processing methods. If you add a new model or test type
you will need to update the ResultFinder so it can figure out which 
parser to call for your model or test.

The current expectation is that each model will have its own processing
methods for each supported test_type. Currently, step and etas processing
is in separate source code files.

## Results directory Contents
2007-08-01 - ntest_format_1 results
2010-03-01 - last format 1 result
2010-07-05 - missing results file
2010-11-22 - example of format 2 results (with STEP and ETAS tags)
2012-05-28 - no result file found
2016-01-30 - missing step results in format 2 (ETAS only)
2017-03-03 - missing step results in format 2 (ETAS only)

