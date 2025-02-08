import unittest
import sys
import os
import io
import libcst as cst

from libcst.display import dump
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from PythonTester.Mutator.MutationGenerator import MutationGenerator

class MutationGeneratorTester(unittest.TestCase):
    generator = None
    converter = None


    def setUp(self):
        self.file_source = "/OriginalFiles/HelloCode/HelloWorld.py"
        self.test_source = "/OriginalFiles/HelloCodeTests/"

    def testStartup(self):
        self.generator = MutationGenerator(self.file_source, self.file_source)
        self.converter = self.generator.converter

    def testPopulation(self):
        self.assertIsNotNone(self.generator)
        self.assertIsNotNone(self.converter)

    # def testParse(self):
    #     self.converter.getTree()




        
