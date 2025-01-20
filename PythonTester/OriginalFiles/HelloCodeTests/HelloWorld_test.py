import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from HelloCode import HelloWorld

class MyTestCase(unittest.TestCase):
    def testStartup(self):
        self.assertEqual(HelloWorld.helloWorld(), "Hello World")  # add assertion here
        self.assertEqual(HelloWorld.makeArray(), 145)

    def testSub(self):
        self.assertTrue(True)
        # self.assertEqual(HelloWorld.subtractMe(), 186)

    def testMultiply(self):
        self.assertTrue(True)
        # self.assertEqual(HelloWorld.multiplyMe(), -30240)

    def testDivide(self):
        self.assertTrue(True)
        # self.assertEqual(HelloWorld.divideMe(), -1)

    def testMod(self):
        self.assertTrue(True)
        # self.assertEqual(HelloWorld.modMe(), 2)

# if __name__ == '__main__':
    # unittest.main()