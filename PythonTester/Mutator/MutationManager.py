import multiprocessing
import importlib
import sys
import unittest
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

def manageMutations(file_source, test_source):
    module_to_del = file_source.replace('/', '.')
    module_to_del = module_to_del[:-2].strip('.')
    del sys.modules[module_to_del]
    q = multiprocessing.Queue()
    startupP = multiprocessing.Process(target=runMutationTest, args=(q, test_source,))
    startupP.start()
    startupP.join()
    importlib.import_module(module_to_del)
    result = q.get()
    return result

def runMutationTest(q, test_source):
    test_suite = unittest.TestLoader().discover(parent + test_source, '*_test.py')
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    resultDict = {}
    resultDict["errorCount"] = len(result.errors)
    resultDict["failedCount"] = len(result.failures)
    resultDict["unexpectedSuccesses"] = len(result.unexpectedSuccesses)
    resultDict["allPassed"] = result.wasSuccessful()
    resultDict["testsRun"] = result.testsRun

    q.put(resultDict)