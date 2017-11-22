import NTestFormats
import TestResult
import os
import datetime
import glob

#
#
# Multiformat parsers have general form
# main routine at top
# Then test to determine which format to call, early or late format
#

def find_testresult_dirs(test_result_list, test_result_dir):
    """
    expected result list
    path to results files
    """
    #
    # Determine whether testdirectory exists
    #

    for trday in test_result_list:
        curdir = test_result_dir + "/" + trday.testDate
        if os.path.exists(curdir):
            trday.test_result_file_path = curdir
            trday.test_result_file_name = curdir
            trday.status = trday.RESDIR_FOUND
        else:
            trday.test_result_file_path = curdir
            trday.test_result_file_name = curdir
            trday.status = trday.RESDIR_NOTFOUND
    return test_result_list


def find_testresult_files(test_result_list, test_result_name):
    """
    input a list of test_result objects.
    Create a file teamplate for them
    Save the template
    Search the directory
    Save the number of matching files
    Save array of matching files
    Save selectedfile
    Assign to returned testresult object

    This methods passes in a string used in the test_result_name, which is used
    to create a result file template

    """
    #
    # Loop through all testdates with directories
    #
    for tr in test_result_list:
        if tr.status == tr.RESDIR_FOUND:
            #
            # The csep test result files names differ slightly in places (NTest,N-Test)
            # one in test result file names, and one is in the xml file.
            #
            tr = find_ntest_result_file_name(tr, test_result_name)
            if tr.status == tr.RESDIR_FOUND:
                pass #
                print "Result File Name lookup - succeeded:", tr.testDate, tr.status, tr.test_result_file_name,tr.result_file_template
            else:
                pass #print "Result File Name lookup - failed:",tr.testDate,tr.status,tr.test_result_file_name,tr.result_file_template

    return test_result_list


def find_ntest_result_file_name(testresult,test_result_name):
    """
    This is the top level entry script that you call with an ntest_result_file.
    This method call two alternative file name construction routines, based on the format in use
    on the testdate represented by this object.

    """
    format_end_date = "2010-03-02"
    res = testresult.testDate.split("-")
    testday = datetime.datetime(int(res[0]),int(res[1]),int(res[2]))
    res = format_end_date.split("-")
    end_f1 = datetime.datetime(int(res[0]),int(res[1]),int(res[2]))
    if testday < end_f1:
        testresult = find_early_ntest_result_file_name(testresult,test_result_name)
        if testresult == None:
            print "Returning None Early Format Result Filename", testresult.testDate
            testresult.status = testresult.rfnotfound
    else:
        testresult = find_later_ntest_result_file_name(testresult,test_result_name)
        if testresult == None:
            print "Returning None Later Format Result Filename",testresult.testDate
            testresult.status = testresult.rfnotfound

    return testresult


def find_early_ntest_result_file_name(testresult,test_result_name):
    """
    input directory name
    processing:
    search file for results file and return found fielname
    """
    result_file_template = "%s/scec.csep.RELMTest.rTest_%s_ETAS_*-fromXML.xml.*"%(testresult.test_result_file_path,
                                                                                     test_result_name)
    testresult.result_file_template = result_file_template
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
            testresult.list_of_testfile_matches.append(short_file_name)
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
            testresult.test_result_file_name = cur_file
            testresult.status = testresult.RESFILE_FOUND
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
            testresult.list_of_testfile_matches.append(short_file_name)
            if ".meta" in short_file_name:
                pass
            else:
                testresult.test_result_file_name = short_file_name
                testresult.status = testresult.RESFILE_FOUND
                #
                # This assumes the singl non-metafile is the result file of interest.
    else: # no files found
        testresult.status = testresult.RESFILE_NOTFOUND

    #
    # Check whether file found, if not set status not found
    #
    testresult.number_of_testfile_matches = len(testresult.list_of_testfile_matches)

    selected_file = testresult.test_result_file_path + "/" + testresult.test_result_file_name
    if testresult.status != testresult.RESFILE_FOUND:
        testresult.status = testresult.RESFILE_NOTFOUND
    elif not os.path.exists(selected_file):
        print "Found test result file name, but does not exist",selected_file
        testresult.status = testresult.RESFILE_NOTFOUND
    return testresult


def find_later_ntest_result_file_name(testresult,test_result_name):
    """
    input directory name
    processing:
    search file for results file and return found fielname
    """
    result_file_template = "%s/scec.csep.AllModelsSummary.all.rTest_%s.xml.*"%(testresult.test_result_file_path,
                                                                               test_result_name)
    names = glob.glob(result_file_template)
    for name in names:
        #
        # this takes the first file found that matches the tempalte
        # separates it into head,tail
        # and assigns the tail as the filename of the result file found
        #
        # Remove xml file path
        #
        short_file_name = os.path.split(name)[1]
        testresult.list_of_testfile_matches.append(short_file_name)
        if ".meta" in short_file_name:
            pass
        else:
            testresult.test_result_file_name = short_file_name
            testresult.status = testresult.RESFILE_FOUND

    #
    # Check whether file found, if not set status not found
    #
    testresult.number_of_testfile_matches = len(testresult.list_of_testfile_matches)
    selected_file = testresult.test_result_file_path + "/" + testresult.test_result_file_name
    if testresult.status != testresult.RESFILE_FOUND:
        testresult.status = testresult.RESFILE_NOTFOUND
    elif not os.path.exists(selected_file):
        print "Found test result file name, but does not exist",selected_file
        testresult.status = testresult.RESFILE_NOTFOUND
    #print "returning trobject as:",testresult
    #print "selected_file",selected_file
    return testresult