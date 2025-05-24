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
import time
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
        timeoutMutants = []
        currentMutants = 0

        # # Start of Try/Except for time limit
        # # try 
        # with open(self.config, 'r', encoding='utf-8') as fd:
        #     config = yaml.safe_load(fd)
        # file_timeouts = config.get('timeouts', {})
        # yaml_default_timeout = file_timeouts.get('default', None)
        # cli_default_timeout = kwargs.get('default_timeout', None)

        
        if 'file_source' not in kwargs:
            with open(self.config, 'r', encoding='utf-8') as fd:
                file_source = yaml.safe_load(fd)['file_source']
                fd.close()
        else:
            file_source = kwargs['file_source']
        if 'test_source' not in kwargs:
            with open(self.config, 'r', encoding='utf-8') as fd:
                test_source = yaml.safe_load(fd)['test_source']
                fd.close()
        else:
            test_source = kwargs['test_source']
        if file_source == "":
            raise Exception("File source not found")
        if test_source == "":
            raise Exception("Test source not found")
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
        # set file or default timeout
        
        # print("Filename: " + filename)
        # file_timeout = (
        #     file_timeouts.get(filename, None)
        #     or yaml_default_timeout
        #     or cli_default_timeout
        #     or None
        # )
        # if file_timeout is not None:
        #     start_time = time.monotonic()
        #     end_time = start_time + file_timeout
        #     print(f"Running mutation for {filename} with timeout = {file_timeout}s")
        # else:
        #     end_time = None
        #     print(f"Running mutation for {filename} with NO timeout")
        #start printing progress_bar here
        with progressbar.ProgressBar(maxval=totalMutants, redirect_stdout=True).start() as progress_bar:
            for tree_generator in tree_generator_array:
                # if end_time is not None:
                #     if time.monotonic() > end_time:
                #         print("Timeout reached, stopping mutation testing")
                #         break
                try: 
                    for i in range(tree_generator.retNumMutants()):
                        # not sure how to deal with the progress bar here when the process is terminated, seems to just say 34/34 even though it terminated early
                        filename = os.path.relpath(tree_generator.file_path, os.path.dirname(self.config)).replace("\\", "/")


                        mutation_type = tree_generator.mutantTypes[i]   
                        method_name = tree_generator.mutationObjects[i]     
                        print(method_name)   
                        file_timeout = (
                            kwargs.get('default_timeout', None)
                            or self.get_mutation_timeout(filename, mutation_type, method_name)
                        )

                        if file_timeout is not None:
                            time_to_go = file_timeout
                        else:
                            time_to_go = None

                        if time_to_go is not None:
                            print(f"Running mutant {i} of {filename} with timeout = {time_to_go}s")
                        else:
                            print(f"Running mutant {i} of {filename} with NO timeout")
                        tree_generator.loadMutatedCode(i)    
                        result = self.manageMutations(tree_generator.file_path, test_source, suppressOut, suppressErr, time_to_go)
                        currentMutants += 1
                        # print(result)
                        if not result:
                            print(f"\033[33mTimeout mutant at index {i} (type {mutation_type})\033[0m")
                            timeoutMutants.append(tree_generator.mutantNodes[i])
                            tree_generator.loadOriginalCode()
                            currentMutants += 1
                            progress_bar.update(i + 1)
                            continue

                        if (result["allPassed"] is False):
                            killedMutants += 1
                            if not genReport:
                                print("\033[32mCorrectly failed test\033[0m")
                                progress_bar.update(i + 1)
                            else:
                                self.updateReport("garbage")
                        else:
                            # survivingMutants.append(tree_generator.nodes[i]) # add more helpful info here

                            # Temporary fix. Identify what needs to be appeneded here. 
                            survivingMutants.append(tree_generator.mutantNodes[i])
                            if not genReport:
                                print("\033[31mERROR Test Is Passing\033[0m")
                                progress_bar.update(i + 1)
                            else:
                                self.updateReport("garbage but bad")
                        tree_generator.loadOriginalCode()
                # except TimeoutError:
                #     print("Timeout reached, stopping mutation testing for this file and restoring original code")
                #     tree_generator.loadOriginalCode()
                except Exception as e:
                    tree_generator.loadOriginalCode()
                    self.printMutantReport(killedMutants, totalMutants, survivingMutants, timeoutMutants, streamToPrintTo)
                    raise e
        self.printMutantReport(killedMutants, totalMutants, survivingMutants, timeoutMutants, streamToPrintTo)
        return True
        # Except: 
        # Code for once timeout
        

    def obtainTrees(self, file_source):
        excluded_files = []
        tree_generator_array =  []
        with open(self.config, 'r', encoding='utf-8') as fd:
            excluded_files = yaml.safe_load(fd)['exclusions']['files']
            fd.close()
        for filename in os.listdir(os.path.normpath(os.path.join(parent, file_source))):
            generator = None
            if filename.endswith('.py') and filename != "__init__.py" and not any(filename in d['filename'] for d in excluded_files):
                generator = MutationGenerator(os.path.join(file_source, filename), self.config)
                tree_generator_array.append(generator)
        return tree_generator_array

    def printMutantReport(self, killedMutants, totalMutants, survivingMutants, timeoutMutants, streamToPrintTo = None):
            print("Successfully killed " + "{:.2f}".format(float(killedMutants)/totalMutants*100) + "% of mutations", file=streamToPrintTo)
            if(survivingMutants == []): 
                print("No surviving mutants", file=streamToPrintTo)
            else:
                print("Surviving Mutants: " + str(len(survivingMutants)), file=streamToPrintTo)
                for mutant in survivingMutants:
                    print(mutant)# file=streamToPrintTo)  
                    # Update line to print out line numbers of mutants/original+mutated lines
                    # print("Line Number: " + str(mutant.lineNumber) + "\tColumn Number: " + str(mutant.colNumber), file=streamToPrintTo)
            if not timeoutMutants:
                print("No timeout mutants", file=streamToPrintTo)
            else:
                print(f"Timeout Mutants: {len(timeoutMutants)}", file=streamToPrintTo)
                for mutant in timeoutMutants:
                    print(mutant)

    def generateReport(self, file_source, test_source, report_directory, report_filename):
        # determine what file to put this report in/how to name the file
        # make file in folder
        # save report location to class variable
        self.reportFile = os.path.normpath(os.path.join(os.path.join(parent, report_directory), report_filename))
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

    def manageMutations(self, file_path, test_source, suppressOut=True, suppressErr=True, timeout=None):
        module_to_del = file_path.replace('\\', '.')
        module_to_del = module_to_del.replace('/', '.')
        module_to_del = module_to_del[:-2].strip('.')
        if module_to_del in sys.modules:
            del sys.modules[module_to_del]
        
        ctx = multiprocessing.get_context("spawn")
        q = ctx.Queue()
        startupP = ctx.Process(target=self.runMutationTest, args=(q, parent + test_source, suppressOut, suppressErr))

        startupP.start()
        startupP.join(timeout)
        if startupP.is_alive():
            startupP.terminate()
            startupP.join()
            return
        importlib.import_module(module_to_del)
        result = q.get()
        return result

    def runMutationTest(self, q, test_source, suppressOut=True, suppressErr=True):
        streamOut = io.StringIO() if suppressOut else sys.stdout
        streamErr = io.StringIO() if suppressErr else sys.stderr
        with contextlib.redirect_stdout(streamOut):
            with contextlib.redirect_stderr(streamErr):
                # time.sleep(1)
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
        
    def get_mutation_timeout(self, filename, mutation_type, method_name=None):
        with open(self.config, 'r', encoding='utf-8') as fd:
            config = yaml.safe_load(fd)

        default_timeout = config.get('timeouts', {}).get('default_timeout', None)
        files = config.get('timeouts', {}).get('files', [])

        # Normalize input path to match keys
        project_root = os.path.normpath(os.path.dirname(self.config))
        input_path = os.path.normpath(filename)
        rel_input = os.path.relpath(input_path, start=project_root).replace("\\", "/")

        matched_entry = None
        for entry in files:
            config_key = list(entry.keys())[0]
            normalized_key = os.path.normpath(config_key).replace("\\", "/").lstrip("./")
            if rel_input == normalized_key or rel_input.lstrip("./") == normalized_key:
                matched_entry = entry
                break

        if matched_entry:
            file_config = matched_entry[list(matched_entry.keys())[0]]
            file_default = file_config.get('default_timeout', default_timeout)

            methods = file_config.get('methods', [])
            method_entry = next((m for m in methods if method_name in m), None) if method_name else None
            if method_entry:
                return method_entry[method_name]

            mutants = file_config.get('mutants', [])
            mutant_entry = next((m for m in mutants if mutation_type in m), None)
            if mutant_entry:
                return mutant_entry[mutation_type]

            return file_default

        return default_timeout







