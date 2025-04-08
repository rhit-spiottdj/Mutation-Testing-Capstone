import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from SimplerHelloCode import SimplerHelloWorld

class MyTestCase(unittest.TestCase):
    def test_simpler_hello_world(self):
        self.assertEqual(SimplerHelloWorld.helloWorld(), -1)
