import os
from datetime import datetime, timezone
import yaml
from cryptography.fernet import Fernet
import logging

class UserID:
    user = ""
    myauth = None
    current = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(current)
    config = path  + "/config.yaml"
    mutationPath = ""
    logger = None

    suite = None

    def __init__(self, logger, auth):
        self.myauth = auth
        self.logger = logger

    def login(self, user, password):
        if(self.myauth.verify_user(user, password, True)):
            self.user = user
            self.logMessage('Logged on successfully.')
            print("Login succesfull!\n")
            return True
        else:
            self.logMessage('Attempted to log on unsuccesfully.')
            print("Failed to login, try again.\n")
        return False
    
    def logout(self):
        if(self.user != ""):
            print("Logged off successfully.\n")
            self.logMessage('Logged off successfully.')
            self.user = ""
            return True
        else: 
            self.logMessage('Attempted to log off unsuccesfully.')
        return False
    
    def addMutation(self, mutation):
        if(self.user == ""):
            return False
        with open(self.config, 'r', encoding='utf-8') as fd:
            self.mutationPath = yaml.safe_load(fd)['mutations']
            fd.close()
        with open(self.path + "/" + self.mutationPath, 'a', encoding='utf-8') as fd:
            cryptMutation = self.encrypt(mutation)
            fd.write(cryptMutation + '\n')
            fd.close()
        print('Added new mutation: "' + mutation + '" to the list of mutations.\n')
        self.logMessage('Added new mutation: "' + mutation + '" to the list of mutations.')
        return True
    
    def fetchLogPath(self):
        with open(self.config, 'r', encoding='utf-8') as fd:
            self.logPath = yaml.safe_load(fd)['data_log']
            fd.close()
    
    def logMessage(self, message):
        # self.fetchLogPath()
        # with open(self.path + "/" + self.logPath, 'a', encoding='utf-8') as fd:
        #     time = datetime.now(timezone.utc)
        #     fd.write("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S") + " UTC\n")
        if(self.user == ""):
            self.logger.info('No current authenticated user, %s\n\n', message)
        else:
            self.logger.info('User: "%s", %s\n\n', self.user, message)

    def encrypt(self, data):
        key = Fernet.generate_key()
        self.suite = Fernet(key) #This is the key
        encryptedData = self.suite.encrypt(bytes(data, encoding="utf-8"))
        return str(encryptedData)

    def decrypt(self, encryptedData):
        data = str(self.suite.decrypt(bytes(encryptedData, encoding="utf-8")))
        print("Decrypted: " + data + "\n")
        return data
