import os
from datetime import datetime, timezone
import yaml
from miniauth.auth import MiniAuth
from cryptography.fernet import Fernet

class UserID:
    user = ""
    myauth = None
    current = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(current)
    config = path  + "/config.yaml"
    mutationPath = ""
    logPath = ""

    suite = None

    def __init__(self, auth):
        self.myauth = auth

    def login(self, user, password):
        self.fetchLogPath()
        if(self.myauth.verify_user(user, password, True)):
            self.user = user
            self.logMessage('User: "' + self.user + '", logged on successfully.\n\n')
            return True
        else:
            self.logMessage('User: "' + user + '", attempted to log on unsuccesfully.\n\n')
        return False
    
    def logout(self):
        self.fetchLogPath()
        if(self.user != ""):
            self.logMessage('User: "' + self.user + '", logged off successfully.\n\n')
            self.user = ""
            return True
        else: 
            self.logMessage('User: "' + self.user + '", attempted to log off unsuccesfully.\n\n')
        return False
    
    def addMutation(self, mutation):
        if(self.user == ""):
            return False
        with open(self.config, 'r', encoding='utf-8') as fd:
            self.mutationPath = yaml.safe_load(fd)['mutations']
            fd.close()
        self.fetchLogPath()
        print(self.logPath)
        with open(self.path + "/" + self.mutationPath, 'a', encoding='utf-8') as fd:
            cryptMutation = self.encrypt(mutation)
            fd.write(cryptMutation + '\n')
            fd.close()
        self.logMessage('User: "' + self.user + '", Added new mutation: "' + mutation + '" to the list of mutations.\n\n')
        return True
    
    def fetchLogPath(self):
        with open(self.config, 'r', encoding='utf-8') as fd:
            self.logPath = yaml.safe_load(fd)['data_log']
            fd.close()
    
    def logMessage(self, message):
        with open(self.path + "/" + self.logPath, 'a', encoding='utf-8') as fd:
            time = datetime.now(timezone.utc)
            fd.write("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S") + " UTC\n")
            fd.write(message)
            fd.close()

    def encrypt(self, data):
        key = Fernet.generate_key()
        self.suite = Fernet(key) #This is the key
        encryptedData = self.suite.encrypt(bytes(data, encoding="utf-8"))
        return str(encryptedData)

    def decrypt(self, encryptedData):
        data = str(self.suite.decrypt(bytes(encryptedData, encoding="utf-8")))
        print("Decrypted: " + data + "\n")
        return data
