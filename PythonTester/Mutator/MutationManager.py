import multiprocessing
import importlib
import sys
import unittest
import os
import Mutator.MutationGenerator as MutationGenerator

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

def generateMutations():
    file_source = None
    test_source = None
    excluded_files = []
    test_tree_array = []
    survivingMutants = []
    killedMutants = 0
    totalMutants = 0
    with open(parent + "/config.txt", 'r', encoding='utf-8') as fd:
        file_source = fd.readline().strip()
        test_source = fd.readline().strip()
        fd.close()
    if file_source == "" or test_source == "":
        raise Exception("File or test source not found")
    with open(parent + "/excluded_config.txt", 'r', encoding='utf-8') as fd:
        excluded_files = fd.read().splitlines()
        fd.close()
    for filename in os.listdir(parent + file_source):
        if filename.endswith('.py') and filename != "__init__.py" and filename not in excluded_files:
            test_tree_array.append(MutationGenerator.MutationTree(file_source + filename))
    for test_tree in test_tree_array:
        test_tree.basicMutateTree()
        try:
            for test_tree in test_tree_array:
                totalMutants += test_tree.retMutationLength()
                for i in range(test_tree.retMutationLength()):
                    test_tree.loadMutatedCode(i)
                    result = manageMutations(test_tree.file_path, test_source)
                    print(result)
                    print(test_tree.nodes[i])
                    if(result["allPassed"] is False):
                        killedMutants += 1
                        print("\033[32mCorrectly failed test\033[0m")
                    else:
                        survivingMutants.append(test_tree.nodes[i])
                        print("\033[31mERROR Test Is Passing\033[0m")
                    test_tree.loadOriginalCode()
        except Exception as e:
            test_tree.loadOriginalCode()
            print("Successfully killed " + "{:.2f}".format(float(killedMutants)/totalMutants*100) + "% of mutations")
            print(str(len(survivingMutants)) + " Surviving Mutants: ")
            for mutant in survivingMutants:
                print(mutant)  # Update this line to print out line numbers of mutants
            raise e
    print("Successfully killed " + "{:.2f}".format(float(killedMutants)/totalMutants*100) + "% of mutations")
    print(str(len(survivingMutants)) + " Surviving Mutants: ")
    for mutant in survivingMutants:
        print(mutant)  # Update this line to print out line numbers of mutants

def obtainTrees():
    return []

def manageMutations(file_path, test_source):
    module_to_del = file_path.replace('\\', '.')
    module_to_del = module_to_del.replace('/', '.')
    module_to_del = module_to_del[:-2].strip('.')
    if module_to_del in sys.modules:
        del sys.modules[module_to_del]
    
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()
    startupP = ctx.Process(target=runMutationTest, args=(q, parent + test_source))

    startupP.start()
    startupP.join()
    importlib.import_module(module_to_del)
    result = q.get()
    return result

def runMutationTest(q, test_source):
    test_suite = unittest.TestLoader().discover(test_source, '*_test.py')
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    resultDict = {}
    resultDict["errorCount"] = len(result.errors)
    resultDict["failedCount"] = len(result.failures)
    resultDict["unexpectedSuccesses"] = len(result.unexpectedSuccesses)
    resultDict["allPassed"] = result.wasSuccessful()
    resultDict["testsRun"] = result.testsRun
    q.put(resultDict)