import ast

class HelloTree():

    operations = []
    variables = []
    values = []
    tree = None

    def __init__(self):
    
        with open('HelloWorld.py', 'r') as fd:
            code = fd.read()
        
            self.tree = ast.parse(code)

    def traverseTree(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Add):
                self.operations.append("+")
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    self.variables.append(node.id)

    def retOperations(self):
        return self.operations
    
    def retVariables(self):
        return self.variables
    
    def retValues(self):
        return self.values

# def main():
#     helloTree()

# if __name__ == '__main__':
#     main()