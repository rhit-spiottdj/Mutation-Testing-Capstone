import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from calculator import Calculator

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.c = Calculator()
        return super().setUp()
    
    def test_sum(self):
        self.assertEqual(self.c.sum(1, 1), 2)

    def test_subtract(self):
        self.assertEqual(self.c.subtract(0, 1), -1)


    def test_multiply(self):
        self.assertEqual(self.c.multiply(10, 0), 0)


    def test_division(self):
        self.assertEqual(self.c.divide(1, 0), 'Can not divide by zero.')


    def test_square_root(self):
        self.assertEqual(self.c.sqrt(-4), 'Invalid input')


    def test_invalid_value(self):
        self.assertEqual(self.c.sum('a', 'b'), 'Invalid input')
        self.assertEqual(self.c.subtract('a', 'b'), 'Invalid input')
        self.assertEqual(self.c.multiply('a', 'b'), 'Invalid input')
        self.assertEqual(self.c.divide('a', 'b'), 'Invalid input')
        self.assertEqual(self.c.square('a'), 'Invalid input')
        self.assertEqual(self.c.sqrt('a'), 'Invalid input')

    def test_memory(self):
        self.c.reset_memory()

        self.assertEqual(self.c.sum(0), 0)
        self.assertEqual(self.c.sum(1), 1)
        self.assertEqual(self.c.sum(1), 2)

        self.c.reset_memory()

        self.assertEqual(self.c.subtract(0), 0)
        self.assertEqual(self.c.subtract(1), -1)
        self.assertEqual(self.c.subtract(1), -2)

        self.c.reset_memory()

        self.assertEqual(self.c.multiply(1, 1), 1)
        self.assertEqual(self.c.multiply(2), 2)
        self.assertEqual(self.c.multiply(2), 4)

        self.c.reset_memory()

        self.assertEqual(self.c.divide(20, 2), 10)
        self.assertEqual(self.c.divide(2), 5)
        self.assertEqual(self.c.divide(5), 1)

        self.c.reset_memory()

        self.assertEqual(self.c.square(2), 4)
        self.assertEqual(self.c.square(), 16)
        self.assertEqual(self.c.square(), 256)

        self.c.reset_memory()

        self.assertEqual(self.c.sqrt(256), 16)
        self.assertEqual(self.c.sqrt(), 4)        
        self.assertEqual(self.c.sqrt(), 2)