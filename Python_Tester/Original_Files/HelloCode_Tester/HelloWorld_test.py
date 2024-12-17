import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from HelloCode import HelloWorld

class MyTestCase(unittest.TestCase):
    def test_startup(self):
        self.assertEqual(HelloWorld.helloWorld(self), "Hello World")  # add assertion here
        self.assertEqual(HelloWorld.makeArray(self), 145)

if __name__ == '__main__':
    unittest.main()