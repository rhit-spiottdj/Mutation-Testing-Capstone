import os
import yaml
import datetime
from miniauth.auth import MiniAuth

class UserID:
    user = ""
    myauth = None
    current = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(current)
    config = path  + "/config.yaml"
    mutationPath = ""
    logPath = ""

    def __init__(self, auth):
        self.myauth = auth

    def login(self, user, password):
        if(self.myauth.verify_user(user, password, True)):
            self.user = user
            return True
        return False
        
    def logout(self, user):
        if(self.user == user):
            self.user = ""
            return True
        return False
    
    def addMutation(self, mutation):
        if(self.user == ""):
            return False
        with open(self.config, 'r', encoding='utf-8') as fd:
            self.mutationPath = yaml.safe_load(fd)['mutations']
            fd.close()
        with open(self.config, 'r', encoding='utf-8') as fd:
            self.logPath = yaml.safe_load(fd)['data_log']
            fd.close()
        print(self.logPath)
        with open(self.path + "/" + self.mutationPath, 'a', encoding='utf-8') as fd:
            fd.write(mutation + '\n')
            fd.close()
        with open(self.path + "/" + self.logPath, 'a', encoding='utf-8') as fd:
            fd.write("Timestamp: " + str(datetime.datetime.now()) + "\n")
            fd.write('User: "' + self.user + '", Added new mutation: "' + mutation + '" to the list of mutations.\n\n')
            fd.close()
        return True