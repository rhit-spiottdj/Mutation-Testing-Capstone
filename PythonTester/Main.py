import os
import argparse
import shutil
import sys
import getpass
import logging
import time
from datetime import datetime
import difflib
import yaml
from pathlib import Path
from miniauth.auth import MiniAuth
import Mutator.MutationManager as Manager
from Auth.UserID import UserID


def check_unknown_flags(parser, argv):
    # Parse known args, leave unknown untouched
    _, unknown = parser.parse_known_args(argv)

    if unknown:
        # Get the list of valid flags
        all_flags = [
            opt
            for action in parser._actions
            for opt in action.option_strings
            if opt.startswith("-")
        ]

        for arg in unknown:
            if arg.startswith("-"):  # looks like a flag
                suggestions = difflib.get_close_matches(arg, all_flags, n=3, cutoff=0.6)
                sys.stderr.write(f"error: unrecognized argument {arg!r}\n")
                if suggestions:
                    sys.stderr.write(f"Did you mean: {', '.join(suggestions)}?\n")
                parser.print_help()
                sys.exit(2)    

parser = argparse.ArgumentParser(description='Mutation test code given a code and test source')
parser.add_argument('-f', '--files', dest='files', type=str, help='The relative file path to the source code directory')
parser.add_argument('-t', '--tests', dest='tests', type=str, help='The relative file path to the test code directory')
parser.add_argument('-p', '--print', dest='print', action='store_true', help='Print the mutated code\'s output to the console')
parser.add_argument('-e', '--error', dest='error', action='store_true', help='Print the mutated code\'s errors to the console')
parser.add_argument('-r', '--report', dest='report', action='store_true', help='Generate mutation report file')
parser.add_argument('-m', '--modify', dest='modify', action='store_true', help='Attempt to login to change list of mutations')
parser.add_argument('--timeout', dest='timeout', type=int, default=None, help='Optional global timeout (in seconds) for each file\'s mutation loop. Files can override via config.')

def generate_default_config():
    DEFAULT_CONFIG_TEXT = """\
# Relative path to source code directory
# file_source: "File Path Here"

# Relative path to test code directory
# test_source: "Test Path Here"

# Items to exclude from mutation
exclusions:
#   directories:
  files:
      - filename: "__init__.py"
        entire_file: true
#     - filename: "File Name Here"
#       entire_file: true/false
#       methods:
#         - "Method Name Here"
#       operators:
#         - "Operator Here"

# The relative path where the mutation report will be generated
report_directory: "/MutationReports/"

# The filename of the generated report
report_filename: "output.txt"

# Encrypted log of mutations added by users
mutations: "mutations.txt"

# Where operator mutation options are defined
mutation_map: "mutationMap.txt"

# Can set default timeout in seconds overall, per file, per method, per mutant type, or none with null
timeouts:
  default_timeout: null
#   files:
#     - Relative File Path Here:
#         default_timeout: 20
#         methods:
#           - makeArray: 0.0000001
#           - divideMe: 0.01
#         mutants:
#           - IF: 0.001
#           - SUBTRACT: 0
"""
    try:
        cfg_path = Path.cwd() / "config.yaml"
        cfg_path.write_text(DEFAULT_CONFIG_TEXT, encoding="utf-8")
        print(f"Wrote fresh commented config to {cfg_path}")
    except Exception as e:
        print("Could not create config file, terminating application")
        print(e)
        sys.exit(1)


def main():
    auth = MiniAuth('users.db') #Here we would fetch a real database to read from
    config_data = None

    logger = logging.getLogger(__name__)
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(filename="MutationTesting.log", encoding='utf-8', level=logging.INFO,
                        filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S UTC')

    userID = UserID(logger, auth)
    userID.logMessage("Application started")

    check_unknown_flags(parser, sys.argv[1:])
  
    args = parser.parse_args()

    cwd = os.getcwd()
    try:
        with open(cwd + "/config.yaml", 'r', encoding='utf-8') as fd:
            config_data = yaml.safe_load(fd)
            fd.close()
    except FileNotFoundError:
        logger.critical("Config file not found, generating default\n")
        print("Config file not found, generating default")
        generate_default_config()
        with open(cwd + "/config.yaml", 'r', encoding='utf-8') as fd:
            config_data = yaml.safe_load(fd)
            fd.close()
    
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
        absPath = os.path.normpath(os.path.join(cwd, args.files))
        if os.path.exists(absPath) is False:
            logger.critical("File path: %s does not exist\n", args.files)
            print("File path does not exist")
            sys.exit(1)
        files = args.files
    else:
        if 'file_source' not in config_data:
            logger.critical("File path not specified\n")
            print("File path not specified")
            sys.exit(1)
        files = config_data['file_source']
    if args.tests:
        absPath = os.path.normpath(os.path.join(cwd, args.tests))
        if os.path.exists(absPath) is False:
            logger.critical("Test path: %s does not exist\n", args.tests)
            print("Test path does not exist")
            sys.exit(1)
        tests = args.tests
    else:
        if 'test_source' not in config_data:
            logger.critical("Test path not specified\n")
            print("Test path not specified")
            sys.exit(1)
        tests = config_data['test_source']
        
        
    kwargs['file_source'] = files
    kwargs['test_source'] = tests
    kwargs['default_timeout'] = args.timeout

    if not args.print:
        kwargs['suppressOut'] = True
    if not args.error:
        kwargs['suppressErr'] = True
    if args.report:
        kwargs['genReport'] = True
    
    manager = Manager.MutationManager()
    logger.info("\nBeginning mutation testing with file directory: %s\nAnd test directory: %s\n", files, tests)
    if (manager.generateMutations(**kwargs)):
        logger.info("\nCompleted mutation testing with file directory: %s\nAnd test directory: %s\nTerminating application\n", files, tests)   
    
if __name__ == '__main__':
    main()