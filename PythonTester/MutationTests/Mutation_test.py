import unittest
import sys
import os
import io

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import MutationManager

class MutationGeneratorTester(unittest.TestCase):
    def setUp(self):
        self.file_source = "/OriginalFiles/HelloCode/"
        self.test_source = "/OriginalFiles/HelloCodeTests/"
        self.test_tree_array = MutationManager.obtainTrees(self.file_source)
    
    def tearDown(self):
        for test_tree in self.test_tree_array:
            test_tree.loadOriginalCode()
            with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, test_tree.original_code)

    def testStartup(self):
        for test_tree in self.test_tree_array:
            test_tree.loadOriginalCode()
            self.assertIsNotNone(test_tree)
            result = MutationManager.manageMutations(test_tree.file_path, self.test_source)
            try:
                self.assertTrue(result["allPassed"])
            except AssertionError as e:
                with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e
        
    def testOriginalTree(self):
        for test_tree in self.test_tree_array:
            test_tree.loadOriginalCode()
            test_tree.traverseTree()
            try:
                self.assertEqual(test_tree.retAdd(), ["+", "+", "+"])
                self.assertEqual(test_tree.retSub(), ["-", "-", "-"])
                self.assertEqual(test_tree.retMulti(), ["*", "*", "*"])
                self.assertEqual(test_tree.retDiv(), ["/", "/", "/"])
                self.assertEqual(test_tree.retMod(), ["%", "%"])
            except AssertionError as e:
                with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e

    def testFirstMutation(self):
        test_tree = self.test_tree_array[0]
        test_tree.basicMutateTree()
        test_tree.loadMutatedCode(0)
        with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, test_tree.original_code)
        result = MutationManager.manageMutations(test_tree.file_path, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\033[32mCorrectly failed test\033[0m")
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m")
            test_tree.loadOriginalCode()
            print("Mutated code:")
            print(test_tree.mutations[0])
            with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, test_tree.original_code) 
            raise e
    
    def testPrintReport(self):
        stream = io.StringIO()
        MutationManager.printMutantReport(1, 2, [1], streamToPrintTo=stream)
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
        MutationManager.generateMutations(**kwargs)
        stream_content = stream.getvalue()
        self.assertEqual(stream_content, "Successfully killed 100.00% of mutations\nNo surviving mutants\n")