import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import HelloTree
from Original_Files.HelloCode_Tester import HelloWorld_test as Test

test_tree = None

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_tree = HelloTree.HelloTree()

    def testStartup(self):
        self.assertIsNotNone(self.test_tree)
        self.assertTrue(Test.MyTestCase())
        
    def testOriginalTree(self): 
        self.test_tree.traverseTree()
        self.assertEqual(self.test_tree.retOperations(), ["+", "+", "+"])
        self.assertEqual(self.test_tree.retVariables(), ["testArray", "rM", "rM"])
        self.assertEqual(self.test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])

    def testFirstMutation(self):
        self.test_tree.basicMutateTree()
        self.test_tree.loadMutatedCode(0)
        try:
            self.assertFalse(Test.MyTestCase())
        except AssertionError:
            self.assertRaises(BaseException, Test.MyTestCase())
            print("Successfully raised exception")
            self.test_tree.loadOriginalCode()
        with open(parent + '/Original_Files/HelloCode/HelloWorld.py', 'r', encoding='utf-8') as fd:
            code = fd.read()
            self.assertEqual(code, self.test_tree.original_code) 

    def testAllMutationVariations(self):
        self.test_tree.basicMutateTree()
        for i in range(self.test_tree.retMutationLength()):
            self.test_tree.loadMutatedCode(i)
            if (i == 0):
                self.assertEqual(self.test_tree.retOperations(), ["-", "+", "+"])
            if (i == 1):
                self.assertEqual(self.test_tree.retOperations(), ["+", "-", "+"])
            if (i == 2):
                self.assertEqual(self.test_tree.retOperations(), ["+", "+", "-"])
            try:
                self.assertFalse(Test.MyTestCase())
            except AssertionError:
                self.assertRaises(BaseException, Test.MyTestCase())
                print("Successfully raised exception")
            self.test_tree.loadOriginalCode()

        

                

#     def testMutateStartup(self):
#         test_tree = HelloTree.HelloTree()
#         self.assertIsNotNone(test_tree)
#         test_tree.basicMutateTree()
#         self.assertEqual(test_tree.retOperations(), ["-", "-", "-"])
#         self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "rM"])
#         self.assertEqual(test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])

if __name__ == '__main__':
    unittest.main()