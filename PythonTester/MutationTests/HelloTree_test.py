import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import HelloTree
from OriginalFiles.HelloCodeTests import HelloWorld_test as Test

class HelloTreeTester(unittest.TestCase):
    def setUp(self):
        with open(parent + "/config.txt", 'r', encoding='utf-8') as fd:
            self.file_source = fd.readline().strip()
        self.test_tree = HelloTree.HelloTree(self.file_source)

    def testStartup(self):
        self.assertIsNotNone(self.test_tree)
        self.assertTrue(Test.MyTestCase())
        
    def testOriginalTree(self): 
        self.test_tree.traverseTree()
        print(self.test_tree.retOperations())
        self.assertEqual(self.test_tree.addop, ["+", "+", "+"])
        # self.assertEqual(self.test_tree.retVariables()[0:3], ["testArray", "rM", "rM"])
        # self.assertEqual(self.test_tree.retValues()[0:6], [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])


    def testFirstMutation(self):
        self.test_tree.basicMutateTree()
        self.test_tree.loadMutatedCode(0)
        print("Testing first mutation:")
        try:
            self.assertFalse(Test.MyTestCase())
            print("\tCorrectly failed test")
        except AssertionError:
            try:
                self.assertRaises(BaseException, Test.MyTestCase())
                print("\tSuccessfully raised exception")
            except AssertionError:
                print("\tError: Mutation passed all tests")
        self.test_tree.loadOriginalCode()
        print("\tRestored original code for next mutation")
        with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
            code = fd.read()
            self.assertEqual(code, self.test_tree.original_code) 

    def testAllMutationVariations(self):
        self.test_tree.basicMutateTree()
        # print("Testing all mutations:")
        for i in range(self.test_tree.retMutationLength()):
            self.test_tree.loadMutatedCode(i)
            print(self.test_tree.nodes[i])
            self.assertNotEqual(self.test_tree.nodes[i], self.test_tree.mutated_nodes[i])
            try:
                self.assertFalse(Test.MyTestCase())
                print("\tMutation " + str(i) + " correctly failed test")
            except AssertionError:
                try:
                    self.assertRaises(BaseException, Test.MyTestCase())
                    print("\tMutation " + str(i) + " Successfully raised exception")
                except AssertionError:
                    print("\tError: Mutation " + str(i) + " passed all tests")
            self.test_tree.loadOriginalCode()
            print("\tRestored original code for next mutation")

        

                

#     def testMutateStartup(self):
#         test_tree = HelloTree.HelloTree()
#         self.assertIsNotNone(test_tree)
#         test_tree.basicMutateTree()
#         self.assertEqual(test_tree.retOperations(), ["-", "-", "-"])
#         self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "rM"])
#         self.assertEqual(test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])

# if __name__ == '__main__':
    # unittest.main()