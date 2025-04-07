import unittest
import sys
import os
import logging

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
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename="AuthTests.log", encoding='utf-8', level=logging.INFO,
                        filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.generator = MutationGenerator(self.file_source, self.file_source)
        self.converter = self.generator.converter

    def testPopulation(self):
        self.logger.info("Running parsing population test")
        self.assertIsNotNone(self.generator)
        self.assertIsNotNone(self.converter)
        self.logger.info("Done running parsing population test")



        
