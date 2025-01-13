import ast
import os

class HelloTree:
    operations = []
    addop = []
    subop = []
    variables = []
    values = []
    tree = None
    original_code = ""
    mutated_code = ""
    C = ""
    # List of Individual mutations
    mutations = []
    # List of nodes linked with list of single mutations before mutation
    nodes = []
    # List of nodes after mutation linked with mutations
    mutated_nodes = []
    file_source = ""

    def __init__(self, fs):
        # VERY IMPORTANT STEP!!!!!
        # Establish path to original file
        self.C = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.file_source = fs

        with open(self.C + self.file_source, 'r', encoding='utf-8') as fd:
            self.original_code = fd.read()


            self.tree = ast.parse(self.original_code)
            
            # Important to print out the syntax of node tree
            # print(ast.dump(self.tree, indent=4)) ##Used for understanding utilization of ast methods

    def loadMutatedCode(self, i):
        with open(self.C + self.file_source, 'w', encoding='utf-8') as fd:
            # self.mutated_code = ast.unparse(self.tree)
            # fd.write(self.mutated_code)
            fd.write(self.mutations[i])
            self.tree = ast.parse(self.mutations[i])
            self.traverseTree()

    def loadOriginalCode(self):
        with open(self.C + self.file_source, 'w', encoding='utf-8') as fd:
            fd.write(self.original_code)

    def traverseTree(self):
        self.addop = []
        self.subop = []
        self.variables = []
        self.values = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Add):
                self.addop.append("+")
            if isinstance(node, ast.Sub):
                self.subop.append("-")
            # if isinstance(node, ast.Mult):
            #     self.operations.append("*")
            # if isinstance(node, ast.Div):
            #     self.operations.append("/")
            # if isinstance(node, ast.Mod):
            #     self.operations.append("%")
            # if isinstance(node, ast.Lt):
            #     self.operations.append("<")
            # if isinstance(node, ast.LtE):
            #     self.operations.append("<=")
            # if isinstance(node, ast.Gt):
            #     self.operations.append(">")
            # if isinstance(node, ast.GtE):
            #     self.operations.append(">=")
            # if isinstance(node, ast.Eq):
            #     self.operations.append("==")
            # if isinstance(node, ast.NotEq):
            #     self.operations.append("!=")
            # if isinstance(node, ast.And):
            #     self.operations.append("&&")
            # if isinstance(node, ast.Or):
            #     self.operations.append("||")
            # if isinstance(node, ast.BitAnd):
            #     self.operations.append("&")
            # if isinstance(node, ast.BitOr):
            #     self.operations.append("|")
            # if isinstance(node, ast.Constant):
            #     self.operations.append("Constant")

            # if isinstance(node, ast.Name):
            #     if isinstance(node.ctx, ast.Store):
            #         self.variables.append(node.id)
            if isinstance(node, ast.Assign) or isinstance(node, ast.AugAssign):
                if isinstance(node.value, ast.Constant):
                    self.values.append(node.value.value)
                if isinstance(node.value, ast.Name):
                    self.values.append(node.value.id)
                if isinstance(node, ast.AugAssign):
                    if isinstance(node.target, ast.Name):
                        if isinstance(node.target.ctx, ast.Store):
                            self.variables.append(node.target.id)
                else: 
                    for name in node.targets:
                        if isinstance(name, ast.Name):
                            if isinstance(name.ctx, ast.Store):
                                self.variables.append(name.id)
                if isinstance(node.value, ast.List):
                    temp = []
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant):
                            temp.append(elt.value)
                    self.values.append(temp)

            if isinstance(node, ast.BinOp):
                if isinstance(node.left, ast.Constant):
                    self.values.append(node.left.value)
                if isinstance(node.right, ast.Constant):
                    self.values.append(node.right.value)
                if isinstance(node.left, ast.Name):
                    self.values.append(node.left.id)
                if isinstance(node.right, ast.Name):
                    self.values.append(node.right.id)

    def retOperations(self):
        return self.operations

    def retVariables(self):
        return self.variables

    def retValues(self):
        return self.values
    
    def retMutationLength(self):
        return len(self.mutations) 
    
    def basicMutateTree(self):
        print("Beginning code mutation")
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add):
                    # Store prev node
                    self.nodes.append(node.op)
                    node.op = ast.Sub()
                    ast.fix_missing_locations(node)
                    self.mutations.append(ast.unparse(self.tree))
                    # Store mutated node
                    self.mutated_nodes.append(node.op)
                    node.op = ast.Add()
                    ast.fix_missing_locations(node)
            if isinstance(node, ast.AugAssign):
                if isinstance(node.op, ast.Add):
                    self.nodes.append(node.op)
                    node.op = ast.Sub()
                    ast.fix_missing_locations(node)
                    self.mutations.append(ast.unparse(self.tree))
                    self.mutated_nodes.append(node.op)
                    node.op = ast.Add()
                    ast.fix_missing_locations(node)
                
        self.traverseTree()

def main(code):
    tree = HelloTree(code)
    tree.traverseTree()

# if __name__ == '__main__':
    # main('/OriginalFiles/HelloCode/HelloWorld.py')