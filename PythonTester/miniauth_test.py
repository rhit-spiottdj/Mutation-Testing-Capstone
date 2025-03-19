import unittest
from miniauth.auth import MiniAuth
from PythonTester.Auth.UserID import UserID

class miniauthTester(unittest.TestCase):
    myauth = None
    userId = None
    def setUp(self):
        self.myauth = MiniAuth('users.db')
        self.myauth.create_user('testuser', '123')
        self.userId = UserID(self.myauth)


    def tearDown(self):
        self.myauth.delete_user('testuser')

    def testamIMini(self):
        self.assertTrue(self.myauth.verify_user('testuser', '123', True))
        self.assertFalse(self.myauth.verify_user('testuser', '124', True))

    def testLogInOut(self):
        self.assertTrue(self.userId.login('testuser', '123'))
        self.assertTrue(self.userId.logout())

    def testAddMutation(self):
        self.assertFalse(self.userId.addMutation("* -> /"))
        self.userId.login('testuser', '123')
        self.assertTrue(self.userId.addMutation("/ -> *"))
        self.assertTrue(self.userId.logout())

        