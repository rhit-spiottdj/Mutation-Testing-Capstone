import unittest
import sys
import os
import io
import libcst as cst

from libcst.display import dump
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from PythonTester.Mutator.MutationManager import MutationManager
# Mutator import MutationManager

code_line_num = -1
code_col_num = -1
og_node = None
new_node = None
mutation_map = {
    "Add()" : "Subtract()",
    "AddAssign()" : "SubtractAssign()",
    "Subtract()" : "Add()",
    "SubtractAssign()" : "AddAssign()",
    "Multiply()" : "Divide()",
    "MultiplyAssign()" : "DivideAssign()",
    "Divide()" : "Multiply()",
    "DivideAssign()" : "MultiplyAssign()",
    "Modulo()" : "Multiply()",
    "ModuloAssign()" : "MultiplyAssign()",
    "BitAnd()" : "BitOr()",
    "BitOr()" : "BitAnd()",
}
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class MutationGeneratorTester(unittest.TestCase):
    def setUp(self):
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
                self.assertTrue(result["allPassed"])
            except AssertionError as e:
                with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e

    def testFirstMutation(self):
        tree_generator = self.tree_generator_array[0]
        tree_generator.basicMutateTree()
        tree_generator.loadMutatedCode(0)

        with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, tree_generator.original_code)
        result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\033[32mCorrectly failed test\033[0m")
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m")
            tree_generator.loadOriginalCode()
            print("Mutated code:")
            print(tree_generator.mutations[0])
            with open(parent + tree_generator.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, tree_generator.original_code) 
            raise e
    
    def testPrintReport(self):
        stream = io.StringIO()
        self.manager.printMutantReport(1, 2, [1], streamToPrintTo=stream)
        stream_content = stream.getvalue()
        self.assertEqual(stream_content, "Successfully killed 50.00% of mutations\n1 Surviving Mutants: \n1\n")

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
        self.assertEqual(stream_content, "Successfully killed 100.00% of mutations\nNo surviving mutants\n")

        tree_generator = self.tree_generator_array[0]
        tree_generator.basicMutateTree()
        
        for i in range(tree_generator.retMutationLength()):
            tree_generator.loadMutatedCode(i)
            
            global code_line_num, code_col_num, og_node, new_node
            code_line_num = tree_generator.retLineNum()[i]
            code_col_num = tree_generator.retColNum()[i]
            og_node = tree_generator.retNodes()[i]

            self.visitor = VisitNodes()
            self.metaDataVisitor = cst.MetadataWrapper(tree_generator.retTree())
            self.metaDataVisitor.visit(self.visitor)


            result = self.manager.manageMutations(tree_generator.file_path, self.test_source)
            print(result)
            print(tree_generator.nodes[i])
            try:
                self.assertEqual(mutation_map[og_node], new_node)
                self.assertFalse(result["allPassed"])
                print("\t\033[32mCorrectly failed test\033[0m")
            except AssertionError as e:
                print("\033[31mERROR Test Is Passing\033[0m")
                print("Mutated code:")
                print(tree_generator.retMutations()[i])
                tree_generator.loadOriginalCode()
                with open(parent + test_ttree_generatorree.file_path, 'r', encoding='utf-8') as fd:
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
        


        

class VisitNodes(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)
    global code_line_num, code_col_num, new_node
    

    def visit_BinaryOperation(self, node):
        global code_line_num, code_col_num, new_node
        pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start

        # print('Node type: BinOp\nFields: ', node.field)
        # print('Line Number: ', pos.line)
        # print('Column Number: ', pos.column)
        # print('BinOp: ', dump(node.operator))
        # print('Checking line number: ', code_line_num)
        # print('Checking column number: ', code_col_num)

        if code_line_num == pos.line and (code_col_num == pos.column or code_col_num + 1 == pos.column):
            # print("Printing node.operator in binary op: ", dump(node.operator))
            new_node = dump(node.operator)
            return
        
    def visit_AugAssign(self, node):
        global code_line_num, code_col_num, new_node
        pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start

        # print('Node type: BinOp\nFields: ', node.field)
        # print('Line Number: ', pos.line)
        # print('Column Number: ', pos.column)
        # print('BinOp: ', dump(node.operator))
        # print('Checking line number: ', code_line_num)
        # print('Checking column number: ', code_col_num)

        if code_line_num == pos.line and (code_col_num == pos.column or code_col_num + 1 == pos.column):
            # print("Printing node.operator in aug assign: ", dump(node.operator))
            new_node = dump(node.operator)
            return
