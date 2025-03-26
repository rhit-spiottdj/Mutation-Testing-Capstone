import datetime
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
        tree_generator_array = self.obtainTrees(file_source)
        
        for tree_generator in tree_generator_array:
            tree_generator.generateMutants()
            totalMutants += tree_generator.retNumMutants()
        
        if genReport:
            # obtain report folder from config and pass in to generateReport
            with open(self.config, 'r', encoding='utf-8') as fd:
                report_directory = yaml.safe_load(fd)['report_directory']
                report_filename = yaml.safe_load(fd)['report_filename']
                fd.close()
            self.generateReport(file_source, test_source, report_directory, report_filename)

        #start printing progress_bar here
        with progressbar.ProgressBar(maxval=totalMutants, redirect_stdout=True).start() as progress_bar:
            for tree_generator in tree_generator_array:
                try: 
                    for i in range(tree_generator.retNumMutants()):
                        tree_generator.loadMutatedCode(i)
                        result = self.manageMutations(tree_generator.file_path, test_source, suppressOut, suppressErr)
                        currentMutants += 1
                        # print(result)
                        # print(test_tree.nodes[i])
                        if(result["allPassed"] is False):
                            killedMutants += 1
                            if not genReport:
                                print("\033[32mCorrectly failed test\033[0m")
                                progress_bar.update(currentMutants)
                            else:
                                self.updateReport("garbage")
                        else:
                            survivingMutants.append(tree_generator.nodes[i]) # add more helpful info here
                            if not genReport:
                                print("\033[31mERROR Test Is Passing\033[0m")
                                progress_bar.update(currentMutants)
                            else:
                                self.updateReport("garbage but bad")
                        tree_generator.loadOriginalCode()
                except Exception as e:
                    tree_generator.loadOriginalCode()
                    self.printMutantReport(killedMutants, totalMutants, survivingMutants, streamToPrintTo)
                    raise e
        self.printMutantReport(killedMutants, totalMutants, survivingMutants, streamToPrintTo)
        return True

    def obtainTrees(self, file_source):
        excluded_files = []
        tree_generator_array =  []
        with open(self.config, 'r', encoding='utf-8') as fd:
            excluded_files = yaml.safe_load(fd)['exclusions']['files']
            fd.close()
        for filename in os.listdir(parent + file_source):
            generator = None
            if filename.endswith('.py') and filename != "__init__.py" and not any(filename in d['filename'] for d in excluded_files):
                generator = MutationGenerator(file_source + filename, self.config)
                tree_generator_array.append(generator)
        return tree_generator_array

    def printMutantReport(self, killedMutants, totalMutants, survivingMutants, streamToPrintTo = None):
            print("Successfully killed " + "{:.2f}".format(float(killedMutants)/totalMutants*100) + "% of mutations", file=streamToPrintTo)
            if(survivingMutants == []): 
                print("No surviving mutants", file=streamToPrintTo)
            else:
                print(str(len(survivingMutants)) + " Surviving Mutants: ", file=streamToPrintTo)
                for mutant in survivingMutants:
                    print(mutant, file=streamToPrintTo)  # Update this line to print out line numbers of mutants/original+mutated lines

    def generateReport(self, file_source, test_source, report_directory, report_filename):
        # determine what file to put this report in/how to name the file
        # make file in folder
        # save report location to class variable
        self.reportFile = parent + report_directory + report_filename
        with open(self.reportFile, 'w', encoding='utf-8') as fd:
            fd.write("Timestamp: " + str(datetime.datetime.now()) + "\n")
            fd.write("File Source: " + file_source + "\n")
            fd.write("Test Source: " + test_source + "\n\n")
            fd.close()
        # close? file
        # could keep the open file in the class semipermanently and close it when done mutating, but that's dangerous
        # could open and close it every time it updates but that's inefficient
        return
    
    def updateReport(self, thingToAddToReport):
        with open(self.reportFile, 'r', encoding='utf-8') as fd:
            fd.write(thingToAddToReport + "\n")
            fd.close()
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