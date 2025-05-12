import unittest
import sys
import os
import io
import libcst as cst
from unittest.mock import patch, MagicMock
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from PythonTester.Mutator.MutationManager import MutationManager

code_line_num = -1
code_col_num = -1


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class MutationGeneratorTester(unittest.TestCase):
    def setUp(self):
        # Temporary sources
        self.file_source = "/OriginalFiles/HelloCode/"
        self.test_source = "/OriginalFiles/HelloCodeTests/"

        self.manager = MutationManager()
        self.tree_generator_array = self.manager.obtainTrees(self.file_source)
    
    def tearDown(self):
        for tree_generator in self.tree_generator_array:
            tree_generator.loadOriginalCode()
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.converter.original_code)

    def testStartup(self):
        for tree_generator in self.tree_generator_array:
            tree_generator.loadOriginalCode()
            self.assertIsNotNone(tree_generator)
            result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
            try:
                print(result)
                self.assertTrue(result["allPassed"])
            except AssertionError as e:
                with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e
            tree_generator.loadOriginalCode()

    def testFirstMutation(self):
        tree_generator = self.tree_generator_array[0]
        tree_generator.generateMutants()
        tree_generator.loadMutatedCode(0)

        with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, tree_generator.converter.original_code)
        result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\033[32mCorrectly failed test\033[0m") # debug
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m") # debug
            tree_generator.loadOriginalCode()
            print("Mutated code:")
            print(tree_generator.mutants[0])
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.converter.original_code) 
            raise e
        tree_generator.loadOriginalCode()
    
    def testPrintReport(self):
        stream = io.StringIO()
        self.manager.printMutantReport(1, 2, [1], 0, streamToPrintTo=stream)
        stream_content = stream.getvalue()
        self.assertIn("Successfully killed 50.00% of mutations\n1 Surviving Mutants: \nNo timeout mutants\n", stream_content)

    def testAllMutationVariations(self):
        stream = io.StringIO()
        kwargs = {}
        kwargs['file_source'] = self.file_source
        kwargs['test_source'] = self.test_source
        kwargs['streamToPrintTo'] = stream
        kwargs['suppressOut'] = True
        kwargs['suppressErr'] = True
        kwargs['genReport'] = False
        self.manager.generateMutations(**kwargs)
        stream_content = stream.getvalue()
        # self.assertEqual(stream_content, "Successfully killed 100.00% of mutations\nNo surviving mutants\n")
        self.assertIn("Successfully killed 100.00% of mutations", stream_content)
        self.assertIn("No surviving mutants", stream_content)

        tree_generator = self.tree_generator_array[0]
        tree_generator.generateMutants()
        
        for i in range(tree_generator.retNumMutants()):
            tree_generator.loadMutatedCode(i)
            
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertNotEqual(code, tree_generator.converter.original_code)

            result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
            print(result)
            try:
                self.assertFalse(result["allPassed"])
                print("\t\033[32mCorrectly failed test\033[0m")
            except AssertionError as e:
                print("\033[31mERROR Test Is Passing\033[0m")
                print("Mutated code:")
                print(tree_generator.retMutations()[i].code)
                tree_generator.loadOriginalCode()
                with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    self.assertEqual(code, tree_generator.retOriginalCode()) 
                raise e
            
            tree_generator.loadOriginalCode()
            print("\tRestored original code for next mutation")
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.retOriginalCode()) 

    def testBoolParse(self):
        expr = cst.parse_expression("True")
        print(expr)
        
    def testFirstMutationRealTimeout(self):
        """
        Test that a real child process timeout occurs with the HelloWorld setup.
        """
        tree_generator = self.tree_generator_array[0]
        tree_generator.generateMutants()
        tree_generator.loadMutatedCode(0)

        # Call manageMutations with extremely small timeout to force termination
        result = self.manager.manageMutations(tree_generator.file_path,
                                            self.test_source,
                                            suppressOut=True,
                                            suppressErr=True,
                                            timeout=0.01)   # tiny timeout

        # Expect result to be None because child process should be forcibly terminated
        self.assertIsNone(result)

        # Always restore original code to avoid affecting other tests
        tree_generator.loadOriginalCode()
        with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertEqual(code, tree_generator.retOriginalCode())

    def testManageMutationsCallsTerminateOnTimeout(self):
        """
        Mock multiprocessing.Process to verify that terminate() is called when child exceeds timeout.
        """
        tree_generator = self.tree_generator_array[0]
        tree_generator.generateMutants()
        tree_generator.loadMutatedCode(0)

        with patch("PythonTester.Mutator.MutationManager.multiprocessing.get_context") as mock_get_context:
            # Create a fake Process
            fake_process = MagicMock()
            fake_process.is_alive.return_value = True  # Simulate child still running after join
            mock_ctx = MagicMock()
            mock_ctx.Process.return_value = fake_process
            mock_get_context.return_value = mock_ctx

            # Call manageMutations (child will be "alive", so parent must call terminate)
            self.manager.manageMutations(
                tree_generator.file_path,
                self.test_source,
                suppressOut=True,
                suppressErr=True,
                timeout=1
            )

            # Assert terminate was called
            fake_process.terminate.assert_called_once()

        # Restore file for safety
        tree_generator.loadOriginalCode()
        with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertEqual(code, tree_generator.retOriginalCode())





        