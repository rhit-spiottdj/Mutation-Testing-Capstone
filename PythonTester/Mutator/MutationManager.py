import multiprocessing
import contextlib
import importlib
import sys
import unittest
import os
import io
import yaml
import progressbar
from Mutator.MutationGenerator import MutationGenerator

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
class MutationManager:
    config = parent + "/config.yaml"

    def generateMutations(self, **kwargs):
        if 'streamToPrintTo' in kwargs:
            streamToPrintTo = kwargs['streamToPrintTo']
        else:
            streamToPrintTo = None
        suppressOut = kwargs['suppressOut'] if 'suppressOut' in kwargs else False
        suppressErr = kwargs['suppressErr'] if 'suppressErr' in kwargs else False
        genReport = kwargs['genReport'] if 'genReport' in kwargs else False
        killedMutants = 0
        totalMutants = 0
        survivingMutants = []
        currentMutants = 0

        if 'file_source' not in kwargs or 'test_source' not in kwargs:
            with open(self.config, 'r', encoding='utf-8') as fd:
                file_source = yaml.safe_load(fd)['file_source']
                test_source = yaml.safe_load(fd)['test_source']
                fd.close()
        else:
            file_source = kwargs['file_source']
            test_source = kwargs['test_source']
        if file_source == "" or test_source == "":
            raise Exception("File or test source not found")
        test_tree_array = self.obtainTrees(file_source)
        
        for test_tree in test_tree_array:
            test_tree.basicMutateTree()
            totalMutants += test_tree.retMutationLength()

        #start printing progress_bar here
        with progressbar.ProgressBar(maxval=totalMutants, redirect_stdout=True).start() as progress_bar:
            for test_tree in test_tree_array:
                try: 
                    for i in range(test_tree.retMutationLength()):
                        test_tree.loadMutatedCode(i)
                        result = self.manageMutations(test_tree.file_path, test_source, suppressOut, suppressErr)
                        currentMutants += 1
                        # print(result)
                        # print(test_tree.nodes[i])
                        if(result["allPassed"] is False):
                            killedMutants += 1
                            if not genReport:
                                print("\033[32mCorrectly failed test\033[0m")
                                progress_bar.update(currentMutants)
                        else:
                            survivingMutants.append(test_tree.nodes[i]) # add more helpful info here
                            if not genReport:
                                print("\033[31mERROR Test Is Passing\033[0m")
                                progress_bar.update(currentMutants)
                        test_tree.loadOriginalCode()
                except Exception as e:
                    test_tree.loadOriginalCode()
                    self.printMutantReport(killedMutants, totalMutants, survivingMutants, streamToPrintTo)
                    raise e
        self.printMutantReport(killedMutants, totalMutants, survivingMutants, streamToPrintTo)

    def obtainTrees(self, file_source):
        excluded_files = []
        test_tree_array =  []
        with open(self.config, 'r', encoding='utf-8') as fd:
            excluded_files = yaml.safe_load(fd)['exclusions']['files']
            fd.close()
        for filename in os.listdir(parent + file_source):
            generator = MutationGenerator(file_source + filename, self.config)
            if filename.endswith('.py') and filename != "__init__.py" and not any(filename in d['filename'] for d in excluded_files):
                test_tree_array.append(generator)
        return test_tree_array

    def printMutantReport(self, killedMutants, totalMutants, survivingMutants, streamToPrintTo = None):
            print("Successfully killed " + "{:.2f}".format(float(killedMutants)/totalMutants*100) + "% of mutations", file=streamToPrintTo)
            if(survivingMutants == []): 
                print("No surviving mutants", file=streamToPrintTo)
            else:
                print(str(len(survivingMutants)) + " Surviving Mutants: ", file=streamToPrintTo)
                for mutant in survivingMutants:
                    print(mutant, file=streamToPrintTo)  # Update this line to print out line numbers of mutants/original+mutated lines

    def generateReport(self):
        return    

    def manageMutations(self, file_path, test_source, suppressOut=True, suppressErr=True):
        module_to_del = file_path.replace('\\', '.')
        module_to_del = module_to_del.replace('/', '.')
        module_to_del = module_to_del[:-2].strip('.')
        if module_to_del in sys.modules:
            del sys.modules[module_to_del]
        
        ctx = multiprocessing.get_context("spawn")
        q = ctx.Queue()
        startupP = ctx.Process(target=self.runMutationTest, args=(q, parent + test_source, suppressOut, suppressErr))

        startupP.start()
        startupP.join()
        importlib.import_module(module_to_del)
        result = q.get()
        return result

    def runMutationTest(self, q, test_source, suppressOut=True, suppressErr=True):
        streamOut = io.StringIO() if suppressOut else sys.stdout
        streamErr = io.StringIO() if suppressErr else sys.stderr
        with contextlib.redirect_stdout(streamOut):
            with contextlib.redirect_stderr(streamErr):
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