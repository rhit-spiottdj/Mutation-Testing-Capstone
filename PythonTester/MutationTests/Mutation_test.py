import unittest
import sys
import os
import io
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from PythonTester.Mutator.MutationManager import MutationManager

code_line_num = -1
code_col_num = -1


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class MutationGeneratorTester(unittest.TestCase):
    def setUp(self):
        # Temporary sources
        self.file_source = "/OriginalFiles/HelloCode/"
        self.test_source = "/OriginalFiles/HelloCodeTests/"

        self.manager = MutationManager()
        self.tree_generator_array = self.manager.obtainTrees(self.file_source)
    
    def tearDown(self):
        for tree_generator in self.tree_generator_array:
            tree_generator.loadOriginalCode()
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.converter.original_code)

    def testStartup(self):
        for tree_generator in self.tree_generator_array:
            tree_generator.loadOriginalCode()
            self.assertIsNotNone(tree_generator)
            result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
            try:
                self.assertTrue(result["allPassed"])
            except AssertionError as e:
                with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e

    def testFirstMutation(self):
        tree_generator = self.tree_generator_array[0]
        tree_generator.generateMutants()
        tree_generator.loadMutatedCode(0)

        with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, tree_generator.converter.original_code)
        result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\033[32mCorrectly failed test\033[0m") # debug
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m") # debug
            tree_generator.loadOriginalCode()
            print("Mutated code:")
            print(tree_generator.mutants[0])
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.converter.original_code) 
            raise e
    
    def testPrintReport(self):
        stream = io.StringIO()
        self.manager.printMutantReport(1, 2, [1], streamToPrintTo=stream)
        stream_content = stream.getvalue()
        self.assertEqual(stream_content, "Successfully killed 50.00% of mutations\n1 Surviving Mutants: \n1\n")

    def testAllMutationVariations(self):
        stream = io.StringIO()
        kwargs = {}
        kwargs['file_source'] = self.file_source
        kwargs['test_source'] = self.test_source
        kwargs['streamToPrintTo'] = stream
        kwargs['suppressOut'] = True
        kwargs['suppressErr'] = True
        kwargs['genReport'] = False
        self.manager.generateMutations(**kwargs)
        stream_content = stream.getvalue()
        self.assertEqual(stream_content, "Successfully killed 100.00% of mutations\nNo surviving mutants\n")

        tree_generator = self.tree_generator_array[0]
        tree_generator.generateMutants()
        
        for i in range(tree_generator.retNumMutants()):
            tree_generator.loadMutatedCode(i)
            
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertNotEqual(code, tree_generator.converter.original_code)

            result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
            print(result)
            try:
                self.assertFalse(result["allPassed"])
                print("\t\033[32mCorrectly failed test\033[0m")
            except AssertionError as e:
                print("\033[31mERROR Test Is Passing\033[0m")
                print("Mutated code:")
                print(tree_generator.retMutations()[i].code)
                tree_generator.loadOriginalCode()
                with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    self.assertEqual(code, tree_generator.retOriginalCode()) 
                raise e
            
            tree_generator.loadOriginalCode()
            print("\tRestored original code for next mutation")
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.retOriginalCode()) 
        