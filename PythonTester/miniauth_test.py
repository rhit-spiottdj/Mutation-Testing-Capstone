import unittest
from miniauth.auth import MiniAuth

class miniauthTester(unittest.TestCase):

    def testamIMini(self):
        myauth = MiniAuth('users.db')
        myauth.create_user('testuser', '123')
        self.assertTrue(myauth.verify_user('testuser', '123'))
        self.assertFalse(myauth.verify_user('testuser', '124'))