import os
import argparse
import Mutator.MutationManager as Manager

parser = argparse.ArgumentParser(description='Mutation test code given a code and test source')
parser.add_argument('-f', '--files', dest='files', type=str, help='The relative file path to the source code directory')
parser.add_argument('-t', '--tests', dest='tests', type=str, help='The relative file path to the test code directory')
parser.add_argument('-p', '--print', dest='print', action='store_true', help='Print the mutated code\'s output to the console')
parser.add_argument('-e', '--error', dest='error', action='store_true', help='Print the mutated code\'s errors to the console')
parser.add_argument('-r', '--report', dest='report', action='store_true', help='Generate mutation report file')

def main():
    # Remove hardcoded file paths once error messages for missing args are implemented
    files = "/OriginalFiles/HelloCode/"
    tests = "/OriginalFiles/HelloCodeTests/"

    args = parser.parse_args()
    
    kwargs = {}
    if args.files:
        files = args.files
        # add file path to config here once config set up better
    if args.tests:
        tests = args.tests
        # add test path to config here once config set up better

    if(files[0] != '/'):
        files = '/' + files

    if(tests[0] != '/'):
        tests = '/' + tests
    
    if(files[-1] != '/'):
        files = files + '/'

    if(tests[-1] != '/'):
        tests = tests + '/'
    
    # remove mandatory file/test reset once config set up better
    cwd = os.getcwd()
    with open(cwd + "/config.txt", 'w', encoding='utf-8') as fd:
            fd.write(files + "\n" + tests)
            fd.close()
            
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