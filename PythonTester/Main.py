import os
import sys
import unittest

def main():
    file = "/OriginalFiles/HelloCode/HelloWorld.py"
    tests = "/OriginalFiles/HelloCodeTests/HelloWorld_test.py"

    if(len(sys.argv) > 1):
        file = sys.argv[1]

    if(len(sys.argv) > 2):
        tests = sys.argv[2]

    if(file[0] != '/'):
        file = '/' + file

    if(tests[0] != '/'):
        tests = '/' + tests

    cwd = os.getcwd()
    with open(cwd + "/config.txt", 'w', encoding='utf-8') as fd:
            fd.write(file + "\n" + tests)

    loader = unittest.TestLoader()
    test_suite = loader.discover("MutationTests", '*_test.py')
    runner = unittest.TextTestRunner()
    runner.run(test_suite)

if __name__ == '__main__':
    main()