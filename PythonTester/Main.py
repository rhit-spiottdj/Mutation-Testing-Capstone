import os
import argparse
import Mutator.MutationManager as Manager
import yaml
import sys

parser = argparse.ArgumentParser(description='Mutation test code given a code and test source')
parser.add_argument('-f', '--files', dest='files', type=str, help='The relative file path to the source code directory')
parser.add_argument('-t', '--tests', dest='tests', type=str, help='The relative file path to the test code directory')
parser.add_argument('-p', '--print', dest='print', action='store_true', help='Print the mutated code\'s output to the console')
parser.add_argument('-e', '--error', dest='error', action='store_true', help='Print the mutated code\'s errors to the console')
parser.add_argument('-r', '--report', dest='report', action='store_true', help='Generate mutation report file')

def main():
    # Remove hardcoded file paths once error messages for missing args are implemented
    config_data = None

    args = parser.parse_args()
    cwd = os.getcwd()
    with open(cwd + "/config.yaml", 'r', encoding='utf-8') as fd:
            config_data = yaml.safe_load(fd)
            fd.close()
    
    kwargs = {}
    if args.files:
        if os.path.exists(cwd + args.files) is False:
            print("File path does not exist")
            sys.exit(1)
        files = args.files
        if(files[0] != '/'):
            files = '/' + files
        if(files[-1] != '/'):
            files = files + '/'
    else:
        files = config_data['file_source']
    if args.tests:
        if os.path.exists(cwd + args.tests) is False:
            print("Test path does not exist")
            sys.exit(1)
        tests = args.tests
        if(tests[0] != '/'):
            tests = '/' + tests
        if(tests[-1] != '/'):
            tests = tests + '/'
    else:
        tests = config_data['test_source']
        
            
    kwargs['file_source'] = files
    kwargs['test_source'] = tests
    if not args.print:
        kwargs['suppressOut'] = True
    if not args.error:
        kwargs['suppressErr'] = True
    if args.report:
        kwargs['genReport'] = True
    

    Manager.generateMutations(**kwargs)

if __name__ == '__main__':
    main()