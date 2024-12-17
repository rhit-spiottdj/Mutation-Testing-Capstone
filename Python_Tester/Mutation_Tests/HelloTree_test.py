import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import HelloTree

class MyTestCase(unittest.TestCase):
        def test_startup(self):
                test_tree = HelloTree.HelloTree()
                self.assertIsNotNone(test_tree)
                test_tree.traverseTree()
                self.assertEqual(test_tree.retOperations(), ["+"])
                self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "rM"])
                self.assertEqual(test_tree.retValues(), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 100, 'x'])

if __name__ == '__main__':
    unittest.main()