import unittest
import importlib
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import MutationManager
from Mutator import MutationGenerator

class MutationGeneratorTester(unittest.TestCase):
    def setUp(self):
        self.test_tree_array = []
        excluded_files = []
        self.file_source = "/OriginalFiles/HelloCode/"
        self.test_source = "/OriginalFiles/HelloCodeTests/"
        with open(parent + "/excluded_config.txt", 'r', encoding='utf-8') as fd:
            excluded_files = fd.read().splitlines()
            fd.close()
        for filename in os.listdir(parent + self.file_source):
            if filename.endswith('.py') and filename != "__init__.py" and filename not in excluded_files:
                self.test_tree_array.append(MutationGenerator.MutationTree(self.file_source + filename))
    
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
            module_to_del = test_tree.file_path.replace('\\', '.')
            module_to_del = module_to_del.replace('/', '.')
            module_to_del = module_to_del[:-2].strip('.')
            if module_to_del in sys.modules:
                del sys.modules[module_to_del]
            test_tree.loadOriginalCode()
            print("\033[31m")
            with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
            print("\033[0m")
            test_tree.traverseTree(True)
            importlib.import_module(module_to_del)
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

    def testAllMutationVariations(self):
        for test_tree in self.test_tree_array:
            test_tree.basicMutateTree()
            for i in range(test_tree.retMutationLength()):
                test_tree.loadMutatedCode(i)
                result = MutationManager.manageMutations(test_tree.file_path, self.test_source)
                print(result)
                print(test_tree.nodes[i])
                
                self.assertNotEqual(test_tree.nodes[i], test_tree.mutated_nodes[i])
                try:
                    self.assertFalse(result["allPassed"])
                    print("\t\033[32mCorrectly failed test\033[0m")
                except AssertionError as e:
                    print("\033[31mERROR Test Is Passing\033[0m")
                    print("Mutated code:")
                    print(test_tree.mutations[i])
                    test_tree.loadOriginalCode()
                    with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                        code = fd.read()
                        fd.close()
                        self.assertEqual(code, test_tree.original_code) 
                    raise e