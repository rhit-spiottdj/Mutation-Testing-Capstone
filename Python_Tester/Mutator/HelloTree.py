import ast
import os

class HelloTree:
    operations = []
    variables = []
    values = []
    tree = None
    original_code = ""
    mutated_code = ""
    C = ""

    def __init__(self):
        # VERY IMPORTANT STEP!!!!!
        # Establish path to original file
        self.C = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        

        with open(self.C + '/Original_Files/HelloCode/HelloWorld.py', 'r') as fd:
            self.original_code = fd.read()

            self.tree = ast.parse(self.original_code)
            #print(ast.dump(self.tree, indent=4)) ##Used for understanding utilization of ast methods

    def loadMutatedCode(self):
        with open(self.C + '/Original_Files/HelloCode/HelloWorld.py', 'w') as fd:
            mutated_code = ast.unparse(self.tree)
            fd.write(self.mutated_code)

    def loadOriginalCode(self):
        with open(self.C + '/Original_Files/HelloCode/HelloWorld.py', 'w') as fd:
            fd.write(self.original_code)

    def traverseTree(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Add):
                self.operations.append("+")
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

    def retOperations(self):
        return self.operations

    def retVariables(self):
        return self.variables

    def retValues(self):
        return self.values

def main():
    tree = HelloTree()
    tree.traverseTree()

if __name__ == '__main__':
    main()