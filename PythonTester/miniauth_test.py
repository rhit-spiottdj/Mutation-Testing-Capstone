import unittest
from miniauth.auth import MiniAuth
from PythonTester.Auth.UserID import UserID
import logging

class miniauthTester(unittest.TestCase):
    myauth = None
    userId = None
    logger = None
    def setUp(self):
        self.myauth = MiniAuth('users.db')
        self.myauth.create_user('testuser', '123')
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename="AuthTests.log", encoding='utf-8', level=logging.INFO,
                        filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.userId = UserID(self.logger, self.myauth)

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

        