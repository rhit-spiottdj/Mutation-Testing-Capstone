import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import HelloTree
from Original_Files.HelloCode_Tester import HelloWorld_test as Test

class MyTestCase(unittest.TestCase):
        def test_startup(self):
                test_tree = HelloTree.HelloTree()
                self.assertIsNotNone(test_tree)
                test_tree.traverseTree()
                self.assertEqual(test_tree.retOperations(), ["+", "+", "+"])
                self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "rM"])
                self.assertEqual(test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])
                self.assertTrue(Test.MyTestCase())
                test_tree.loadMutatedCode()
                try:
                       self.assertFalse(Test.MyTestCase()) ##When running mutated code change this to assertFalse
                except:
                       print("Test case crashed!")
                test_tree.loadOriginalCode()
                with open(parent + '/Original_Files/HelloCode/HelloWorld.py', 'r') as fd:
                       code = fd.read()
                       self.assertEqual(code, test_tree.original_code) 

        def test_mutate_startup(self):
               test_tree = HelloTree.HelloTree()
               self.assertIsNotNone(test_tree)
               test_tree.basicMutateTree()
               self.assertEqual(test_tree.retOperations(), ["-", "-", "-"])
               self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "rM"])
               self.assertEqual(test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])

if __name__ == '__main__':
    unittest.main()