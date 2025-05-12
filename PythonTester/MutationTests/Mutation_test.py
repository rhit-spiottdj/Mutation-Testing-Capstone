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
from PythonTester.Mutator.MutationGenerator import MutationGenerator
from PythonTester.Mutator.NodeTypes import NodeType

class ManagerTester(unittest.TestCase):
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
        self.assertIn("Successfully killed 50.00% of mutations\nSurviving Mutants: 1\nNo timeout mutants\n", stream_content)

    def testKillRate(self):
        stream = io.StringIO()
        self.manager.printMutantReport(1, 2, [1], 0, streamToPrintTo=stream)
        stream_content = stream.getvalue()
        print("The % of surviving mutations is: " + stream_content[20:stream_content.find("%")])
        percentage = float(stream_content[20:stream_content.find("%")])
        self.assertGreaterEqual(percentage, 50.0)

        stream.truncate(0)
        stream.seek(0)
        
        self.manager.printMutantReport(0, 2, [2], 0, streamToPrintTo=stream)
        stream_content = stream.getvalue()
        print("The % of surviving mutations is: " + stream_content[20:stream_content.find("%")])
        percentage = float(stream_content[20:stream_content.find("%")])
        self.assertGreaterEqual(percentage, 0.0)

        stream.truncate(0)
        stream.seek(0)
        
        self.manager.printMutantReport(2, 2, [], 0, streamToPrintTo=stream)
        stream_content = stream.getvalue()
        print("The % of surviving mutations is: " + stream_content[20:stream_content.find("%")])
        percentage = float(stream_content[20:stream_content.find("%")])
        self.assertGreaterEqual(percentage, 100.0)



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
        percentage = float(stream_content[20:stream_content.find("%")])
        self.assertGreaterEqual(percentage, 80.0)
        # self.assertIn("Successfully killed 100.00% of mutations", stream_content)
        # self.assertIn("No surviving mutants", stream_content)

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

    # Test to write raw code and view how it is parsed
    # def testNumParse(self):
    #     expr = cst.parse_expression("1")
    #     print(expr)
        
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
        
class GeneratorTester(unittest.TestCase):
    def setUp(self):
        # Temporary sources
        self.file_source = "/OriginalFiles/HelloCode/"
        config = parent + "/TestConfigs/mapTest.yaml"

        self.generator = MutationGenerator(self.file_source + "HelloWorld.py", config) #Generator for HelloWorld 

    def tearDown(self):
        self.generator.loadOriginalCode()
        with open(parent + self.generator.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertEqual(code, self.generator.converter.original_code)

    def testGetMutationMap(self):
        expectedMap = {
            NodeType.ADD : [NodeType.SUBTRACT],
            NodeType.ADDASSIGN : [NodeType.SUBTRACTASSIGN],
            NodeType.SUBTRACT : [NodeType.ADD],
            NodeType.SUBTRACTASSIGN : [NodeType.ADDASSIGN],
            NodeType.MULTIPLY : [NodeType.DIVIDE],
            NodeType.MULTIPLYASSIGN : [NodeType.DIVIDEASSIGN],
            NodeType.DIVIDE : [NodeType.MULTIPLY],
            NodeType.DIVIDEASSIGN: [NodeType.MULTIPLYASSIGN],
        }
        generatedMap = self.generator.param
        for item in expectedMap.keys():
            for i in range(len(expectedMap[item])):
                self.assertEqual(expectedMap[item][i].name, generatedMap[item.value][i].name)

    def testNumMutants(self):
        self.generator.generateMutants()
        self.assertEqual(self.generator.retNumMutants(), 11)

# class CSTConverterTester(unittest.TestCase):
#     def setUp(self):
#         # Temporary sources
#         self.file_source = "/OriginalFiles/HelloCode/"
#         config = parent + "/TestConfigs/mapTest.yaml"

#         self.generator = MutationGenerator(self.file_source + "HelloWorld.py", config) #Generator for HelloWorld 
#         self.converter = self.generator.converter

#         self.cst_conversion_map = {
#             cst.Add() : NodeType.ADD,
#             cst.AddAssign() : NodeType.ADDASSIGN,
#             cst.Subtract() : NodeType.SUBTRACT,
#             cst.SubtractAssign() : NodeType.SUBTRACTASSIGN,
#             cst.Multiply() : NodeType.MULTIPLY,
#             cst.MultiplyAssign() : NodeType.MULTIPLYASSIGN,
#             cst.Divide() : NodeType.DIVIDE,
#             cst.DivideAssign() : NodeType.DIVIDEASSIGN,
#             cst.Modulo() : NodeType.MODULO,
#             cst.ModuloAssign() : NodeType.MODULOASSIGN,
#             cst.BitAnd() : NodeType.BITAND,
#             cst.BitOr() : NodeType.BITOR,
#             cst.Power() : NodeType.POWER,
#             cst.LessThan() : NodeType.LESSTHAN,
#             cst.GreaterThan() : NodeType.GREATERTHAN,
#             cst.Equal() : NodeType.EQUAL,
#             cst.NotEqual() : NodeType.NOTEQUAL,
#             cst.LessThanEqual() : NodeType.LESSTHANEQUAL,
#             cst.GreaterThanEqual() : NodeType.GREATERTHANEQUAL,
#             cst.Module(body=[cst.SimpleStatementLine(cst.Pass())]) : NodeType.MODULE,
#             cst.EmptyLine() : NodeType.EMPTYLINE,
#             cst.SimpleWhitespace(value=" ") : NodeType.SIMPLEWHITESPACE,
#             cst.Comment(value="# Test comment") : NodeType.COMMENT,
#             cst.Newline() : NodeType.NEWLINE,
#             cst.FunctionDef(name=cst.Name(value="Test"), params=cst.Parameters(), body=cst.IndentedBlock(body=[cst.Name(value="Test")])) : NodeType.FUNCTIONDEF,
#             cst.Name(value="Test") : NodeType.NAME,
#             cst.Parameters() : NodeType.PARAMETERS,
#             cst.IndentedBlock(body=[cst.Name(value="Test")]) : NodeType.INDENTEDBLOCK,
#             cst.TrailingWhitespace() : NodeType.TRAILINGWHITESPACE,
#             cst.SimpleStatementLine(body=[cst.Pass()]) : NodeType.SIMPLESTATEMENTLINE,
#             cst.Expr(value=cst.Name(value="Test")) : NodeType.EXPR,
#             cst.Call(func=cst.Name(value="Test")) : NodeType.CALL,
#             cst.Arg(value=cst.Name(value="Test")) : NodeType.ARG,
#             cst.SimpleString(value="Test") : NodeType.SIMPLESTRING,
#             cst.Return() : NodeType.RETURN,
#             cst.Assign(targets=[cst.AssignTarget(target=cst.Name(value="Test"))], value=cst.Name(value="Test")) : NodeType.ASSIGN,
#             cst.AssignTarget(target=cst.Name(value="Test")) : NodeType.ASSIGNTARGET,
#             cst.List(elements=[cst.Name(value="Test")]) : NodeType.LIST,
#             cst.LeftSquareBracket() : NodeType.LEFTSQUAREBRACKET,
#             cst.Element(value=cst.Name(value="Test")) : NodeType.ELEMENT,
#             cst.Integer(str="10") : NodeType.INTEGER,
#             cst.Comma() : NodeType.COMMA,
#             cst.RightSquareBracket() : NodeType.RIGHTSQUAREBRACKET,
#             cst.BinaryOperation() : NodeType.BINARYOPERATION,
#             cst.For() : NodeType.FOR,
#             cst.AugAssign() : NodeType.AUGASSIGN,
#             cst.UnaryOperation() : NodeType.UNARYOPERATION,
#             cst.Minus() : NodeType.MINUS,
#             cst.Comparison() : NodeType.COMPARISON,
#             cst.ComparisonTarget() : NodeType.COMPARISONTARGET,
#             cst.BooleanOperation() : NodeType.BOOLEANOPERATION,
#             cst.LeftParen() : NodeType.LEFTPAREN,
#             cst.And() : NodeType.AND,
#             cst.RightParen() : NodeType.RIGHTPAREN,
#             cst.Or() : NodeType.OR,
#             cst.IfExp() : NodeType.IFEXP,
#             cst.Is() : NodeType.IS,
#             cst.BitInvert() : NodeType.BITINVERT,
#             cst.Not() : NodeType.NOT,
#             cst.Plus() : NodeType.PLUS,
#             cst.MaybeSentinel() : NodeType.MAYBESENTINEL,
#             cst.ClassDef() : NodeType.CLASSDEF,
#             cst.Param() : NodeType.PARAM,
#             cst.ParamStar() : NodeType.PARAMSTAR,
#             cst.AssignEqual() : NodeType.ASSIGNEQUAL,
#             cst.BaseExpression() : NodeType.BASEEXPRESSION,
#             cst.Annotation() : NodeType.ANNOTATION,
#             cst.BaseParenthesizableWhitespace() : NodeType.BASEPARENTHESIZABLEWHITESPACE,
#             cst.Semicolon() : NodeType.SEMICOLON,
#             cst.BaseCompoundStatement() : NodeType.BASECOMPOUNDSTATEMENT,
#             cst.If() : NodeType.IF,
#             cst.Else() : NodeType.ELSE,
#         }

#     def tearDown(self):
#         self.generator.loadOriginalCode()
#         with open(parent + self.generator.file_path, 'r', encoding='utf-8') as fd:
#             code = fd.read()
#             fd.close()
#             self.assertEqual(code, self.generator.converter.original_code)

#     #TODO: Write tests for the converters methods
#     def testBasicConversion(self):
#         for arg in self.cst_conversion_map.keys():
#             self.assertEqual(self.cst_conversion_map[arg].name, self.converter.convertNode(arg).nodeType.name)
