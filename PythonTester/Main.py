import os
import sys
import Mutator.MutationManager as Manager

def main():
    # Remove hardcoded file paths once error messages for missing args are implemented
    file = "/OriginalFiles/HelloCode/"
    tests = "/OriginalFiles/HelloCodeTests/"

    if(len(sys.argv) > 1):
        file = sys.argv[1]

    if(len(sys.argv) > 2):
        tests = sys.argv[2]

    if(file[0] != '/'):
        file = '/' + file

    if(tests[0] != '/'):
        tests = '/' + tests
    
    if(file[-1] != '/'):
        file = file + '/'

    if(tests[-1] != '/'):
        tests = tests + '/'

    cwd = os.getcwd()
    with open(cwd + "/config.txt", 'w', encoding='utf-8') as fd:
            fd.write(file + "\n" + tests)
            fd.close()
    
    Manager.generateMutations()

if __name__ == '__main__':
    main()