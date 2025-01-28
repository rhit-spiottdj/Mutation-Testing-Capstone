import unittest
import sys
import os
import io
import libcst as cst

from libcst.display import dump

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
}
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import MutationManager

class MutationGeneratorTester(unittest.TestCase):
    def setUp(self):
        self.file_source = "/OriginalFiles/HelloCode/"
        self.test_source = "/OriginalFiles/HelloCodeTests/"
        self.test_tree_array = MutationManager.obtainTrees(self.file_source)
    
    def tearDown(self):
        for test_tree in self.test_tree_array:
            test_tree.loadOriginalCode()
            with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, test_tree.original_code)

    def testStartup(self):
        for test_tree in self.test_tree_array:
            test_tree.loadOriginalCode()
            self.assertIsNotNone(test_tree)
            result = MutationManager.manageMutations(test_tree.file_path, self.test_source)
            try:
                self.assertTrue(result["allPassed"])
            except AssertionError as e:
                with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e
        
    def testOriginalTree(self):
        test_tree = self.test_tree_array[0]
        test_tree.loadOriginalCode()
        test_tree.traverseTree()
        for i in range(len(test_tree.retNodes())):
            global code_line_num, code_col_num, og_node, new_node
            code_line_num = test_tree.retLineNum()[i]
            code_col_num = test_tree.retColNum()[i]
            og_node = test_tree.retNodes()[i]

            self.visitor = VisitNodes()
            self.metaDataVisitor = cst.MetadataWrapper(test_tree.retTree())
            self.metaDataVisitor.visit(self.visitor)
            try:
                self.assertEqual(og_node, new_node)
            except AssertionError as e:
                with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    print(code)
                raise e

    def testFirstMutation(self):
        test_tree = self.test_tree_array[0]
        test_tree.basicMutateTree()
        test_tree.loadMutatedCode(0)

        with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, test_tree.original_code)
        result = MutationManager.manageMutations(test_tree.file_path, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\033[32mCorrectly failed test\033[0m")
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m")
            test_tree.loadOriginalCode()
            print("Mutated code:")
            print(test_tree.mutations[0])
            with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, test_tree.original_code) 
            raise e
    
    def testPrintReport(self):
        stream = io.StringIO()
        MutationManager.printMutantReport(1, 2, [1], streamToPrintTo=stream)
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
        MutationManager.generateMutations(**kwargs)
        stream_content = stream.getvalue()
        self.assertEqual(stream_content, "Successfully killed 100.00% of mutations\nNo surviving mutants\n")

        test_tree = self.test_tree_array[0]
        test_tree.basicMutateTree()
        
        for i in range(test_tree.retMutationLength()):
            test_tree.loadMutatedCode(i)
            
            global code_line_num, code_col_num, og_node, new_node
            code_line_num = test_tree.retLineNum()[i]
            code_col_num = test_tree.retColNum()[i]
            og_node = test_tree.retNodes()[i]

            self.visitor = VisitNodes()
            self.metaDataVisitor = cst.MetadataWrapper(test_tree.retTree())
            self.metaDataVisitor.visit(self.visitor)


            result = MutationManager.manageMutations(test_tree.file_path, self.test_source)
            print(result)
            print(test_tree.nodes[i])
            try:
                self.assertEqual(mutation_map[og_node], new_node)
                self.assertFalse(result["allPassed"])
                print("\t\033[32mCorrectly failed test\033[0m")
            except AssertionError as e:
                print("\033[31mERROR Test Is Passing\033[0m")
                print("Mutated code:")
                print(test_tree.retMutations()[i])
                test_tree.loadOriginalCode()
                with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    self.assertEqual(code, test_tree.retOriginalCode()) 
                raise e
            
            test_tree.loadOriginalCode()
            print("\tRestored original code for next mutation")
            with open(parent + test_tree.file_path, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, test_tree.retOriginalCode()) 
        


        

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
