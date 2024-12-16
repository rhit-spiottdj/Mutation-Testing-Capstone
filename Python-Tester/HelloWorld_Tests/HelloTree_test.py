import unittest
import HelloTree

class MyTestCase(unittest.TestCase):
        def test_startup(self):
                test_tree = HelloTree.HelloTree()
                self.assertIsNotNone(test_tree)
                test_tree.traverseTree()
                self.assertEqual(test_tree.retOperations(), ["+"])
                self.assertEqual(test_tree.retVariables(), ["testArray", "rM", "x", "rM"])
                #self.assertEqual(test_tree.retValues(), ["[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]", "100"])

if __name__ == '__main__':
    unittest.main()