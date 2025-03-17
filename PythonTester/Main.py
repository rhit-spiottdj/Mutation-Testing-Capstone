import os
import argparse
import sys
import logging
import yaml
import Mutator .MutationManager as Manager

parser = argparse.ArgumentParser(description='Mutation test code given a code and test source')
parser.add_argument('-f', '--files', dest='files', type=str, help='The relative file path to the source code directory')
parser.add_argument('-t', '--tests', dest='tests', type=str, help='The relative file path to the test code directory')
parser.add_argument('-p', '--print', dest='print', action='store_true', help='Print the mutated code\'s output to the console')
parser.add_argument('-e', '--error', dest='error', action='store_true', help='Print the mutated code\'s errors to the console')
parser.add_argument('-r', '--report', dest='report', action='store_true', help='Generate mutation report file')

def main():
    config_data = None

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="PythonTester.log", encoding='utf-8', level=logging.DEBUG)

    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # ch.setFormatter(formatter)

    fh = logging.FileHandler('PythonTester.log', mode='a', encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    # logger.addHandler(ch)

    args = parser.parse_args()
    cwd = os.getcwd()
    try:
        with open(cwd + "/config.yaml", 'r', encoding='utf-8') as fd:
            config_data = yaml.safe_load(fd)
            fd.close()
    except FileNotFoundError:
        logger.critical("Config file not found")
        print("Config file not found")
        sys.exit(1)
    
    kwargs = {}
    if args.files:
        if os.path.exists(cwd + args.files) is False:
            logger.critical("File path: %s does not exist", args.files)
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
            logger.critical("Test path: %s does not exist", args.tests)
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
    
    # Write to log file
    logger.info("Beginning mutation testing with file directory: %s\nAnd test directory: %s", files, tests)
    Manager.generateMutations(**kwargs)
    # Write to log file after successful mutation

if __name__ == '__main__':
    main()