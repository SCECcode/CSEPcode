import ResultStatus
import datetime
import os
import glob
import sys
import xml.etree.ElementTree as ET
#
# Define two test result root tags
#

format_1_root_tag_name = "CSEPResult"
format_2_root_tag_name = "CSEPAllModelsSummary"

#
# This top level method, calls the appropriate detailed processing methods, defined below
#
def find_etas_ntest_result(config,expected_result,result_datetime):
    #
    # This method directs the step ntest into time zones, and calls the right
    # parsing method based on the resultDateTime
    #
    etas_ntest_format_1_starttime = config["ETAS"]["etas_ntest_format_1_starttime"]
    etas_ntest_format_1_endtime = config["ETAS"]["etas_ntest_format_1_endtime"]
    etas_ntest_format_2_starttime = config["ETAS"]["etas_ntest_format_2_starttime"]
    etas_ntest_format_2_endtime = config["ETAS"]["etas_ntest_format_2_endtime"]

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

    #
    # This determines which format processing method to call, based on the resultdate
    # Currently only two formats are needed. If a forecast group has more formats defined
    # for the report period, then more elif statements would be added here to call the right
    # processing method. This also assumes the user correctly specifies contigous time zones
    # since essentially not checking is done in the code the the report timezones are contigous
    # and don't overlap
    #
    if res_datetime >= report_start_datetime and res_datetime <= report_end_datetime:
        expected_result = read_etas_ntest_format_1(config,expected_result)
    elif res_datetime >= report2_start_datetime and res_datetime <= report2_end_datetime:
        expected_result = read_etas_ntest_format_2(config,expected_result)
    else:
        print "No parser due to datetime format issues",res_datetime,report2_end_datetime
        expected_result.status = ResultStatus.PARSER_NOT_FOUND

    return expected_result

#
# Second Level Processing Script, one for each STEP,Test,format combination
#
def read_etas_ntest_format_1(config, expected_result):
    """
    This finds the step_ntest files in the first format saved by CSEP
    """
    etas_ntest_result_file_path = config["ETAS"]["etas_ntest_result_file_path"]

    expected_result.test_result_file_path = etas_ntest_result_file_path.replace('"','') + "/" + \
                                            expected_result.resultDateTime

    #print expected_result.test_result_file_path

    if not os.path.isdir(expected_result.test_result_file_path):
        expected_result.status = ResultStatus.DIR_NOT_FOUND
        return expected_result
    else:
        expected_result.status = ResultStatus.FILE_NOT_FOUND

    #
    # Retrieve the ntest string from config file
    #
    etas_ntest_result_name = config["ETAS"]["etas_ntest_result_name"]

    expected_result = find_etas_ntest_result_file_name1(expected_result,
                                                       etas_ntest_result_name.replace('"',''))

    if expected_result.status == ResultStatus.FILE_NOT_FOUND:
        print "File not found by etas_ntest method"
        return expected_result

    #print "Ready to read xml file",expected_result.test_result_file_name

    #
    # Now parse the xml file of the given format
    #

    a_path = expected_result.test_result_file_path + "/" + expected_result.test_result_file_name

    tree = ET.parse(a_path)
    root = tree.getroot()
    # expect roottag with xml file. split it off
    # {http: // www.scec.org / xml - ns / csep / 0.1}CSEPAllModelsSummary
    # with split return ending filename as array 1
    root_tag_base = root.tag.split("}")
    if root_tag_base[1] != format_1_root_tag_name:
        print "Found unexpected Root tag:", root.tag, root_tag_base[1]
        sys.exit(False)
    else:
        for child in root:
            # print "child - resultData",child.tag
            for achild in child:
                # print "achild - NTest",achild.tag
                param_count = 0
                for bchild in achild:
                    #
                    # Construct the TestResult Object with values from XML File
                    # In this old format the test_date is not in the xml file.
                    # Use th test date from the results directory name
                    #
                    res = bchild.tag.split("}")  # Split path from attrib name
                    if "name" == res[1]:
                        expected_result.model_name = bchild.text
                        param_count += 1
                    elif "eventCount" == res[1]:
                        expected_result.eventCount = float(bchild.text)
                        param_count += 1
                    elif "delta1" == res[1]:
                        expected_result.delta1 = float(bchild.text)
                        param_count += 1
                    elif "delta2" == res[1]:
                        expected_result.delta2 = float(bchild.text)
                        param_count += 1
                    elif "eventCountForecast" == res[1]:
                        expected_result.eventCountForecast = float(bchild.text)
                        param_count += 1
                    else:
                        #
                        # Format has several other unused elements, but
                        # description,creationInfo,modificationData,cdfData
                        # we ignore them silently for now.
                        # print "Found Unexpected Test Type",res[1]
                        pass

    if param_count < 5:
        expected_result.status = ResultStatus.DATA_NOT_FOUND
        print "Unexpected param count (expected 5):",param_count
    else:
        expected_result.status = ResultStatus.SUCCESS

    return expected_result


def find_etas_ntest_result_file_name1(expected_result,test_result_name):
     """
     input directory name
     processing:
     search file for results file and return found filname
     """
     result_file_template = "%s/scec.csep.RELMTest.rTest_%s_ETAS_*-fromXML.xml.*"%(expected_result.test_result_file_path,
                                                                                      test_result_name)
     expected_result.result_file_template = result_file_template
     names = glob.glob(result_file_template)
     if len(names) > 2:
         first = True
         cur_file = ""
         max_stat = None
         cur_stat = None
         for name in names:
             # Remove xml file path
             #
             short_file_name = os.path.split(name)[1]
             expected_result.list_of_testfile_matches.append(short_file_name)
             if ".meta" in short_file_name:
                 pass # Skip any meta files
             elif first:
                 max_stat = os.stat(name)
                 cur_file = short_file_name
                 #print "firstfile:",max_stat.st_ctime,cur_file
                 #print max_stat
                 first = False
             else:
                 cur_stat = os.stat(name)
                 #print cur_stat
                 if cur_stat.st_mtime > max_stat.st_mtime:
                     max_stat = cur_stat
                     cur_file = short_file_name
                     #print "foundfile:", max_stat.st_mtime, cur_file
         #
         # Assign return params
         #
         if cur_file != None:
             expected_result.test_result_file_name = cur_file
             expected_result.status = ResultStatus.DATA_NOT_FOUND
         else:
             print "Ntest template search returned null file"
     elif len(names) > 0:
         for name in names:
             #
             # this takes the first file found that matches the tempalte
             # separates it into head,tail
             # and assigns the tail as the filename of the result file found
             #
             short_file_name = os.path.split(name)[1]
             expected_result.list_of_testfile_matches.append(short_file_name)
             if ".meta" in short_file_name:
                 pass
             else:
                 expected_result.test_result_file_name = short_file_name
                 expected_result.status = ResultStatus.DATA_NOT_FOUND
                 #
                 # This assumes the singl non-metafile is the result file of interest.
     else: # no files found
         expected_result.status = ResultStatus.FILE_NOT_FOUND

     #
     # Check whether file found, if not set status not found
     #
     expected_result.number_of_testfile_matches = len(expected_result.list_of_testfile_matches)

     selected_file = expected_result.test_result_file_path + "/" + expected_result.test_result_file_name
     #print "selected result file:",selected_file
     if expected_result.status == ResultStatus.DATA_NOT_FOUND:
        #
        # Check if file existss, if Not set status file not found
        if not os.path.exists(selected_file):
            print "Found test result file name, but does not exist",selected_file
            expected_result.status = ResultStatus.FILE_NOT_FOUND

     return expected_result

#
# The following are the Second Format Processing methods
#
def read_etas_ntest_format_2(config,expected_result):
    """
    This finds the step_ntest files in the first format saved by CSEP
    """
    #print "Processing step ntest format 2"
    etas_ntest_result_file_path = config["ETAS"]["etas_ntest_result_file_path"]

    expected_result.test_result_file_path = etas_ntest_result_file_path.replace('"','') + "/" + \
                                            expected_result.resultDateTime

    #
    # Check if results directory exists, if not return immediately
    #
    if not os.path.isdir(expected_result.test_result_file_path):
        expected_result.status = ResultStatus.DIR_NOT_FOUND
        return expected_result
    else:
        expected_result.status = ResultStatus.FILE_NOT_FOUND

    #
    # Retrieve the ntest string from config file
    #
    etas_ntest_result_name = config["ETAS"]["etas_ntest_result_name"]
    etas_ntest_result_name = etas_ntest_result_name.replace('"','')

    #
    # Retrieve the XML Tag used in the file format, strip quotes from string
    #
    xml_tag_name = config["ETAS"]["etas_ntest_xml_tag_name"]
    xml_tag_name = xml_tag_name.replace('"','')

    #
    # Construct file pathname
    #
    result_file_template = "%s/scec.csep.AllModelsSummary.all.rTest_%s.xml.*"%(expected_result.test_result_file_path,
                                                                               etas_ntest_result_name)
    #print "Result file template:",result_file_template
    names = glob.glob(result_file_template)
    if len(names) < 1:
        expected_result.status = ResultStatus.FILE_NOT_FOUND
        return expected_result

    for name in names:
        #
        # this takes the first file found that matches the tempalte
        # separates it into head,tail
        # and assigns the tail as the filename of the result file found
        #
        # Remove xml file path
        #
        short_file_name = os.path.split(name)[1]
        expected_result.list_of_testfile_matches.append(short_file_name)
        if ".meta" in short_file_name:
            pass
        else:
            expected_result.test_result_file_name = short_file_name
            expected_result.status = ResultStatus.DATA_NOT_FOUND

    #
    # Check whether file found, if not set status not found
    #
    expected_result.number_of_testfile_matches = len(expected_result.list_of_testfile_matches)
    selected_file = expected_result.test_result_file_path + "/" + expected_result.test_result_file_name

    if not os.path.isfile(selected_file):
        print "Found test result file name, but does not exist",selected_file
        expected_result.status = ResultStatus.FILE_NOT_FOUND
        return expected_result

    #
    # Now assemble absolute pathname and parse xml file
    #
    a_path = expected_result.test_result_file_path + "/" + expected_result.test_result_file_name

    #
    #
    #
    #print "parsing path:",a_path
    tree = ET.parse(a_path)
    root = tree.getroot()
    root_tag_base = root.tag.split("}")
    if root_tag_base[1] != format_2_root_tag_name:
        print "Found unexpected Root tag:",root.tag,root_tag_base[1]
        expected_result.status = ResultStatus.DATA_NOT_FOUND
        return expected_result
    else:
        for child in root:
            newres = child.tag.split("}")
            if xml_tag_name == newres[1]:
                for nchild in child:
                    res = nchild.tag.split("}") # Split path from attrib name
                    if "name" == res[1]:
                        expected_result.model_name = nchild.text
                    elif "eventCount" == res[1]:
                        expected_result.eventCount = float(nchild.text)
                    elif "delta1" == res[1]:
                        expected_result.delta1 = float(nchild.text)
                    elif "delta2" == res[1]:
                        expected_result.delta2 = float(nchild.text)
                    elif "eventCountForecast" == res[1]:
                        expected_result.eventCountForecast = float(nchild.text)
                    elif "testDate" == res[1]:
                        expected_result.testDate = nchild.text
                    else:
                        print "Found Unexpected Test Type",nchild.tag
            else:
                print "Found unexpected child tag:","NTest",child.tag

    expected_result.status = ResultStatus.SUCCESS
    return expected_result