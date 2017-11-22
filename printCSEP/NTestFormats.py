#
# Contains methods for parsing CSEP N-Test result file.
#
import TestResult
import NTestFormats
import xml.etree.ElementTree as ET
import datetime
import sys



#
# Define two test result root tags
#

early_root_tag_name = "CSEPResult"
later_root_tag_name = "CSEPAllModelsSummary"


"""
These are the three levels of XML in the early file format
<ns0:CSEPResult xmlns:ns0="http://www.scec.org/xml-ns/csep/0.1">
  <ns0:resultData publicID="smi://org.scec/csep/results/1">
     <ns0:NTest publicID="smi://org.scec/csep/tests/ntest/1">

"""


def parse_testresult_files(test_result_list,test_xml_name):
    """
    input list of test result days with files to parse
    output an updated list of test result day with results parsed
    """
    for oneresult in test_result_list:
        if oneresult.status == oneresult.RESFILE_FOUND:
            oneresult = NTestFormats.parse_testresult_file(oneresult,test_xml_name)
            if oneresult == None:
                print "NTestFormats.parse routine failed for %s : %s/%s" % (oneresult.status,
                                                                            oneresult.test_result_file_path,
                                                                            oneresult.test_result_file_name)

    return test_result_list



def parse_testresult_file(testresult,
                          test_name):
    """
    Select the right parser by checking the format end date.
    Here the end date is hardcoded into this method. Should be moved
    to a better collection point.

    """
    format_end_date = "2010-03-02"

    res = testresult.testDate.split("-")
    testday = datetime.datetime(int(res[0]),int(res[1]),int(res[2]))
    res = format_end_date.split("-")
    end_f1 = datetime.datetime(int(res[0]),int(res[1]),int(res[2]))

    if testday < end_f1:
        #print "Calling Early Form Parser",testresult.testDate
        testresult = parse_early_ntest_result_file(testresult,
                                                    test_name)
    else:
        #print "Calling Late Form Parser",testresult.testDate
        testresult = parse_later_ntest_result_file(testresult,
                                                    test_name)

    return testresult


def parse_early_ntest_result_file(testresult,
                                    test_name):
    #
    # Input test_name
    # Assumes the result_file_path includes the date string
    # Example:
    # Read the xml file
    #
    a_path = testresult.test_result_file_path + "/" + testresult.test_result_file_name

    tree = ET.parse(a_path)
    root = tree.getroot()
    # expect roottag with xml file. split it off
    # {http: // www.scec.org / xml - ns / csep / 0.1}CSEPAllModelsSummary
    # with split return ending filename as array 1
    root_tag_base = root.tag.split("}")
    if root_tag_base[1] != early_root_tag_name:
        print "Found unexpected Root tag:",root.tag,root_tag_base[1]
        sys.exit(False)
    else:
        for child in root:
            #print "child - resultData",child.tag
            for achild in child:
                #print "achild - NTest",achild.tag
                param_count = 0
                for bchild in achild:
                    #
                    # Construct the TestResult Object with values from XML File
                    # In this old format the test_date is not in the xml file.
                    # Use th test date from the results directory name
                    #
                    res = bchild.tag.split("}") # Split path from attrib name
                    if "name" == res[1]:
                        testresult.modelname = bchild.text
                        param_count += 1
                    elif "eventCount" == res[1]:
                        testresult.eventCount = float(bchild.text)
                        param_count += 1
                    elif "delta1" == res[1]:
                        testresult.delta1 = float(bchild.text)
                        param_count += 1
                    elif "delta2" == res[1]:
                        testresult.delta2 = float(bchild.text)
                        param_count += 1
                    elif "eventCountForecast" == res[1]:
                        testresult.eventCountForecast = float(bchild.text)
                        param_count += 1
                    else:
                        #
                        # Format has several other unused elements, but
                        # description,creationInfo,modificationData,cdfData
                        # we ignore them silently for now.
                        #print "Found Unexpected Test Type",res[1]
                        pass

    if param_count < 5:
        testresult.status = testresult.RESFILE_ERROR
        #print "param count:",param_count
    else:
        testresult.status = testresult.RESFILE_OK
    return testresult


def parse_later_ntest_result_file(testresult,
                                  test_name):
    #
    # Input test_name
    # Assumes the result_file_path includes the date string
    # Example:
    # Read the xml file
    #
    a_path = testresult.test_result_file_path + "/" + testresult.test_result_file_name

    #
    #
    #
    tree = ET.parse(a_path)
    root = tree.getroot()
    root_tag_base = root.tag.split("}")
    if root_tag_base[1] != later_root_tag_name:
        print "Found unexpected Root tag:",root.tag,root_tag_base[1]
        sys.exit(False)
    else:
        for child in root:
            newres = child.tag.split("}")
            if test_name == newres[1]:
                for nchild in child:
                    res = nchild.tag.split("}") # Split path from attrib name
                    if "name" == res[1]:
                        testresult.modelname = nchild.text
                    elif "eventCount" == res[1]:
                        testresult.eventCount = float(nchild.text)
                    elif "delta1" == res[1]:
                        testresult.delta1 = float(nchild.text)
                    elif "delta2" == res[1]:
                        testresult.delta2 = float(nchild.text)
                    elif "eventCountForecast" == res[1]:
                        testresult.eventCountForecast = float(nchild.text)
                    elif "testDate" == res[1]:
                        testresult.testDate = nchild.text
                    else:
                        print "Found Unexpected Test Type",nchild.tag
            else:
                print "Found unexpected child tag:","NTest",child.tag

    testresult.status = testresult.RESFILE_OK
    return testresult