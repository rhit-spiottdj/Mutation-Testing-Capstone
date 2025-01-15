import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import MutationManager
from Mutator import HelloTree

class HelloTreeTester(unittest.TestCase):
    def setUp(self):
        with open(parent + "/config.txt", 'r', encoding='utf-8') as fd:
            self.file_source = fd.readline().strip()
            self.test_source = fd.readline().strip()
            fd.close()
        self.test_tree = HelloTree.HelloTree(self.file_source)

    def testStartup(self):
        self.assertIsNotNone(self.test_tree)
        result = MutationManager.manageMutations(self.file_source, self.test_source)
        try:
            self.assertTrue(result["allPassed"])
        except AssertionError as e:
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                print(code)
            raise e
        
    def testOriginalTree(self):
        self.test_tree.traverseTree()
        try:
            self.assertEqual(self.test_tree.retAdd(), ["+", "+", "+"])
            self.assertEqual(self.test_tree.retSub(), ["-", "-", "-"])
            self.assertEqual(self.test_tree.retMulti(), ["*", "*", "*"])
            self.assertEqual(self.test_tree.retDiv(), ["/", "/", "/"])
            self.assertEqual(self.test_tree.retMod(), ["%", "%"])
            # self.assertEqual(self.test_tree.retVariables()[0:3], ["testArray", "rM", "rM"])
            # self.assertEqual(self.test_tree.retValues()[0:6], [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])
        except AssertionError as e:
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                print(code)
            raise e

    def testFirstMutation(self):
        self.test_tree.basicMutateTree()
        self.test_tree.loadMutatedCode(0)
        with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, self.test_tree.original_code)
        result = MutationManager.manageMutations(self.file_source, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\t\033[32mCorrectly failed test\033[0m")
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m" + e)
            self.test_tree.loadOriginalCode()
            print("Mutated code:")
            print(self.test_tree.mutations[0])
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, self.test_tree.original_code) 
            raise e
        self.test_tree.loadOriginalCode()
        print("\tRestored original code for next mutation")
        with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertEqual(code, self.test_tree.original_code) 

    def testAllMutationVariations(self):
        self.test_tree.basicMutateTree()
        for i in range(self.test_tree.retMutationLength()):
            self.test_tree.loadMutatedCode(i)
            result = MutationManager.manageMutations(self.file_source, self.test_source)
            print(result)
            print(self.test_tree.nodes[i])
            
            # if(og == "+"):
            #     self.assertEqual(new, "-")
            # if(og == "-"):
            #     self.assertEqual(new, "+")
            
            self.assertNotEqual(self.test_tree.nodes[i], self.test_tree.mutated_nodes[i])
            try:
                self.assertFalse(result["allPassed"])
                print("\t\033[32mCorrectly failed test\033[0m")
            except AssertionError as e:
                print("\033[31mERROR Test Is Passing\033[0m")
                print("Mutated code:")
                print(self.test_tree.mutations[i])
                self.test_tree.loadOriginalCode()
                with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    self.assertEqual(code, self.test_tree.original_code) 
                raise e
            self.test_tree.loadOriginalCode()
            print("\tRestored original code for next mutation")
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, self.test_tree.original_code) 

        

                

#     def testMutateStartup(self):
#         test_tree = HelloTree.HelloTree()
#         self.assertIsNotNone(test_tree)
#         test_tree.basicMutateTree()
#         self.assertEqual(test_tree.retOperations(), ["-", "-", "-"])
#         self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "rM"])
#         self.assertEqual(test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])

# if __name__ == '__main__':
    # unittest.main()