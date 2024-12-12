import unittest
import HelloWorld

class MyTestCase(unittest.TestCase):
    def test_startup(self):
        self.assertEqual(HelloWorld.HelloWorld(self), "Hello World")  # add assertion here


if __name__ == '__main__':
    unittest.main()
