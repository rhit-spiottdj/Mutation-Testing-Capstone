import os
import argparse
import sys
import getpass
import yaml
from datetime import datetime
from miniauth.auth import MiniAuth
import Mutator.MutationManager as Manager
from Auth.UserID import UserID

parser = argparse.ArgumentParser(description='Mutation test code given a code and test source')
parser.add_argument('-f', '--files', dest='files', type=str, help='The relative file path to the source code directory')
parser.add_argument('-t', '--tests', dest='tests', type=str, help='The relative file path to the test code directory')
parser.add_argument('-p', '--print', dest='print', action='store_true', help='Print the mutated code\'s output to the console')
parser.add_argument('-e', '--error', dest='error', action='store_true', help='Print the mutated code\'s errors to the console')
parser.add_argument('-r', '--report', dest='report', action='store_true', help='Generate mutation report file')
parser.add_argument('-m', '--modify', dest='modify', action='store_true', help='Attempt to login to change list of mutations')

def main():
    auth = MiniAuth('users.db') #Here we would fetch a real database to read from
    userID = UserID(auth)
    userID.logMessage("Application started")
    config_data = None

    args = parser.parse_args()
    cwd = os.getcwd()
    try:
        with open(cwd + "/config.yaml", 'r', encoding='utf-8') as fd:
            config_data = yaml.safe_load(fd)
            fd.close()
    except FileNotFoundError:
        print("Config file not found")
        sys.exit(1)
    
    kwargs = {}
    if args.modify:
        authSuccess = False
        isMutating = True
        i = 0
        while (not authSuccess and i < 3):
            username = input("Username: ")
            pswd = getpass.getpass('Password: ')
            authSuccess = userID.login(username, pswd)
            i += 1
        startTime = datetime.now()
        while (authSuccess and isMutating):
            difference = datetime.now() - startTime
            if (difference.total_seconds()/60 >= 10):
                userID.logout()
                authSuccess = False
            #allow for modification of mutators
            #loop asking them to add multiple mutators? options to add or delete or modify current mutators?
            mutator = input("What mutation would you like to add? ")
            if(mutator == "quit" or mutator == "q" or mutator == "log off"):
                userID.logout()
                isMutating = False
            else:
                userID.addMutation(mutator)
        if(not authSuccess):
            message = "Too many failed login attempts, terminating application."
            print(message + '\n')
            userID.logMessage(message)
        exit()

    if args.files:
        if os.path.exists(cwd + args.files) is False:
            print("File path does not exist")
            sys.exit(1)
        files = args.files
    else:
        files = config_data['file_source']
    if(files[0] != '/'):
        files = '/' + files
    if(files[-1] != '/'):
        files = files + '/'
    if args.tests:
        if os.path.exists(cwd + args.tests) is False:
            print("Test path does not exist")
            sys.exit(1)
        tests = args.tests
    else:
        tests = config_data['test_source']
    if(tests[0] != '/'):
        tests = '/' + tests
    if(tests[-1] != '/'):
        tests = tests + '/'
        
        
    kwargs['file_source'] = files
    kwargs['test_source'] = tests
    if not args.print:
        kwargs['suppressOut'] = True
    if not args.error:
        kwargs['suppressErr'] = True
    if args.report:
        kwargs['genReport'] = True
    
    manager = Manager.MutationManager()
    userID.logMessage("mutation has begun, running tests.")
    if (manager.generateMutations(**kwargs)):
        userID.logMessage("successfully tested mutated code, terminating application.")

if __name__ == '__main__':
    main()