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
        self.assertEqual(HelloWorld.subtractMe(), 186)

    def testMultiply(self):
        self.assertEqual(HelloWorld.multiplyMe(), -30240)

    def testDivide(self):
        self.assertEqual(HelloWorld.divideMe(), -1)

    def testMod(self):
        self.assertEqual(HelloWorld.modMe(), 2)

    def testGreaterThanMe(self):
        self.assertTrue(HelloWorld.greaterThanMe())

    def testLessThanMe(self):
        self.assertTrue(HelloWorld.lessThanMe())

    def testGreaterThanEqualMe(self):
        self.assertTrue(HelloWorld.greaterThanEqualMe())

    def testLessThanEqualMe(self):
        self.assertTrue(HelloWorld.lessThanEqualMe())

    def testEqualMe(self):
        self.assertTrue(HelloWorld.equalMe())

    def testNotEqualMe(self):
        self.assertTrue(HelloWorld.notEqualMe())

    def testAndMe(self):
        self.assertTrue(HelloWorld.andMe())

    def testOrMe(self):
        self.assertTrue(HelloWorld.orMe())

    def testBitwiseAndMe(self):
        self.assertFalse(HelloWorld.bitwiseAndMe())

    def testBitwiseOrMe(self):
        self.assertTrue(HelloWorld.bitwiseOrMe())

    def testTernaryNullOperator(self):
        self.assertIsNotNone(HelloWorld.ternaryNullOperator())
    
    def testChangeStringToEmpty(self):
        self.assertIsNotNone(HelloWorld.changeStringToEmpty())

    def testChangeZeroToOne(self):
        self.assertEqual(HelloWorld.changeZeroToOne(), 0)

    def testChangeOneToZero(self):
        self.assertEqual(HelloWorld.changeOneToZero(), 1)



# if __name__ == '__main__':
    # unittest.main()