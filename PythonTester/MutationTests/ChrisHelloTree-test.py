import unittest
import sys
import os
import ast

code_line_num = -1
var_1 = None
var_2 = None
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Mutator import MutationManager
from Mutator import ChrisHelloTree as HelloTree

class HelloTreeTester(unittest.TestCase):
    def setUp(self):
        with open(parent + "/config.txt", 'r', encoding='utf-8') as fd:
            self.file_source = fd.readline().strip()
            self.test_source = fd.readline().strip()
            fd.close()
        self.test_tree = HelloTree.HelloTree(self.file_source)
        self.visitor = VisitNodes()

    def testStartup(self):
        self.test_tree.loadOriginalCode()
        self.assertIsNotNone(self.test_tree)
        result = MutationManager.manageMutations(self.file_source, self.test_source)
        try:
            self.assertTrue(result["allPassed"])
        except AssertionError as e:
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                print(code)
            raise e
        
    def testOriginalTree(self):
        self.test_tree.loadOriginalCode()
        self.test_tree.traverseTree()
        try:
            self.assertEqual(self.test_tree.retAdd(), ["+", "+", "+"])
            self.assertEqual(self.test_tree.retSub(), ["-", "-", "-"])
            self.assertEqual(self.test_tree.retMulti(), ["*", "*", "*"])
            self.assertEqual(self.test_tree.retDiv(), ["/", "/", "/"])
            self.assertEqual(self.test_tree.retMod(), ["%", "%"])
            # self.assertEqual(self.test_tree.retVariables()[0:3], ["testArray", "rM", "rM"])
            # self.assertEqual(self.test_tree.retValues()[0:6], [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 40, 60, 'x', "Wowzers!", '178'])
        except AssertionError as e:
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                print(code)
            raise e

    def testFirstMutation(self):
        self.test_tree.basicMutateTree()
        self.test_tree.loadMutatedCode(0)

        global code_line_num, var_1,var_2
        code_line_num = self.test_tree.line_num[0]
        print("var_1 and var_2 before running visit on the ith node (node[0])")
        print("var_1: ", var_1)
        print("var_2: ", var_2, "\n")
        self.visitor.visit(self.test_tree.nodes[0])
        print("Finish running visit on the ith node (node[0])")
        print("var_1: ", var_1)
        print("var_2: ", var_2, "\n")
        var_2 = var_1
        var_1 = None
        print("Reassign var_1 to var_2, then var_1 to none")
        print("var_1: ", var_1)
        print("var_2: ", var_2, "\n")
        print("var_1 and var_2 before running visit on the tree")
        self.visitor.visit(self.test_tree.tree)
        print("Finish running visit on the tree")
        print("var_1: ", var_1)
        print("var_2: ", var_2, "\n")

        with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertNotEqual(code, self.test_tree.original_code)
        result = MutationManager.manageMutations(self.file_source, self.test_source)
        print(result)
        try:
            self.assertFalse(result["allPassed"])
            print("\t\033[32mCorrectly failed test\033[0m")
        except AssertionError as e:
            print("\033[31mERROR Test Is Passing\033[0m")
            self.test_tree.loadOriginalCode()
            print("Mutated code:")
            print(self.test_tree.mutations[0])
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, self.test_tree.original_code) 
            raise e
        self.test_tree.loadOriginalCode()
        print("\tRestored original code for next mutation")
        with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
            code = fd.read()
            fd.close()
            self.assertEqual(code, self.test_tree.original_code) 

    def testAllMutationVariations(self):
        self.test_tree.basicMutateTree()
        for i in range(self.test_tree.retMutationLength()):
            self.test_tree.loadMutatedCode(i)
            
            global code_line_num, var_1,var_2
            code_line_num = self.test_tree.line_num[i]
            print("var_1 and var_2 before running visit on the ith node (node[i])")
            print("var_1: ", var_1)
            print("var_2: ", var_2, "\n")
            self.visitor.visit(self.test_tree.nodes[i])
            print("Finish running visit on the ith node (node[i])")
            print("var_1: ", var_1)
            print("var_2: ", var_2, "\n")
            var_2 = var_1
            var_1 = None
            print("Reassign var_1 to var_2, then var_1 to none")
            print("var_1: ", var_1)
            print("var_2: ", var_2, "\n")
            print("Run visit on the current tree")
            self.visitor.visit(self.test_tree.tree)
            print("Finish running visit on the tree")
            print("var_1: ", var_1)
            print("var_2: ", var_2, "\n")

            # global code_line_num, var_1,var_2
            # code_line_num = self.test_tree.line_num[i]
            # self.visitor.visit(self.test_tree.nodes[i])
            # var_2 = var_1
            # var_1 = None
            # print("Finish running visit on the ith node (node[i])\n")
            # print("var_1: ", var_1)
            # print("var_2: ", var_2, "\n")
            # self.visitor.visit(self.test_tree.tree)
            # print("Finish running visit on the tree\n")
            # print("var_1: ", var_1)
            # print("var_2: ", var_2, "\n")
            # if var_2 == ast.Add:
            #     self.assertEqual(var_1, ast.Sub)
            self.assertNotEqual(var_1, var_2)

            var_1 = None
            var_2 = None

            result = MutationManager.manageMutations(self.file_source, self.test_source)
            print(result)
            print(self.test_tree.nodes[i])
            
            try:
                self.assertFalse(result["allPassed"])
                print("\t\033[32mCorrectly failed test\033[0m")
            except AssertionError as e:
                print("\033[31mERROR Test Is Passing\033[0m")
                print("Mutated code:")
                print(self.test_tree.mutations[i])
                self.test_tree.loadOriginalCode()
                with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                    code = fd.read()
                    fd.close()
                    self.assertEqual(code, self.test_tree.original_code) 
                raise e
            
            self.test_tree.loadOriginalCode()
            print("\tRestored original code for next mutation")
            with open(parent + self.file_source, 'r', encoding='utf-8') as fd:
                code = fd.read()
                fd.close()
                self.assertEqual(code, self.test_tree.original_code) 
        


        

class VisitNodes(ast.NodeVisitor):
    def visit_BinOp(self, node):
        global code_line_num, var_1
        print('Node type: BinOp\nFields: ', node._fields)
        print('Line Number: ', node.lineno)
        print('BinOp: ', node.op)
        print(code_line_num)

        if code_line_num == node.lineno:
            print("^ Assign node.op to var_1")

            var_1 = node.op
        print("\n")
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_AugAssign(self, node):
        global code_line_num, var_1

        if code_line_num == node.lineno:
            print('Node type: AugAssign\nFields: ', node._fields)
            print('Line Number: ', node.lineno)
            print('AugAssign: ', node.op)
            print(code_line_num)
            print('\n')
            var_1 = node.op
        ast.NodeVisitor.generic_visit(self, node)