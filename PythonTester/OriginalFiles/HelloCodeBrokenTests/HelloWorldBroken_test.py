import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from HelloCode import HelloWorld

class MyTestCase(unittest.TestCase):
    def testStartup(self):
        self.assertTrue(True)
        self.assertTrue(True)

    def testSub(self):
        self.assertTrue(True)

    def testMultiply(self):
        self.assertTrue(True)

    def testDivide(self):
        self.assertTrue(True)

    def testMod(self):
        self.assertTrue(True)

    def testGreaterThanMe(self):
        self.assertTrue(True)

    def testLessThanMe(self):
        self.assertTrue(True)

    def testGreaterThanEqualMe(self):
        self.assertTrue(True)
    def testLessThanEqualMe(self):
        self.assertTrue(True)
    def testEqualMe(self):
        self.assertTrue(HelloWorld.equalMe())

    def testNotEqualMe(self):
        self.assertTrue(True)
    def testAndMe(self):
        self.assertTrue(True)
    def testOrMe(self):
        self.assertTrue(True)

    def testBitwiseAndMe(self):
        self.assertTrue(True)

    def testBitwiseOrMe(self):
        self.assertTrue(True)

    def testTernaryNullOperator(self):
        self.assertTrue(True)
    
    def testChangeStringToEmpty(self):
        self.assertTrue(True)

    def testChangeZeroToOne(self):
        self.assertTrue(True)
    def testChangeOneToZero(self):
        self.assertTrue(True)



# if __name__ == '__main__':
    # unittest.main()