import os
# import libcst as cst

from Mutator.TreeMutator import TreeMutator
from Mutator.TreeConverter import TreeConverter
from Mutator.NodeTypes import NodeType

class MutationGenerator:

    mutation_map = {
        NodeType.ADD : NodeType.SUBTRACT,
        NodeType.ADDASSIGN : NodeType.SUBTRACTASSIGN,
        NodeType.SUBTRACT : NodeType.ADD,
        NodeType.SUBTRACTASSIGN : NodeType.ADDASSIGN,
        NodeType.MULTIPLY : NodeType.DIVIDE,
        NodeType.MULTIPLYASSIGN : NodeType.DIVIDEASSIGN,
        NodeType.DIVIDE : NodeType.MULTIPLY,
        NodeType.DIVIDEASSIGN: NodeType.MULTIPLYASSIGN,
        NodeType.MODULO : NodeType.MULTIPLY,
        NodeType.MODULOASSIGN : NodeType.MULTIPLYASSIGN,
        NodeType.BITAND: NodeType.BITOR,
        NodeType.BITOR : NodeType.BITAND,
    }

    C = ""
    # mutant_path = ""
    config_path = ""

    converter = None
    tree = None
    mutants = []

    mutator = None
    param = ""
    
    def __init__(self, fs, config):
        # global tree, og_tree
        # VERY IMPORTANT STEP!!!!!
        # Establish path to original file
        self.C = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        
        self.converter = TreeConverter(fs, self.C)
        self.tree = self.converter.getTree()
        self.nodes = [] #Not sure what this is going to do yet

        self.mutator = TreeMutator()
        self.config_path = config
        self.file_path = fs

        with open(self.config_path, 'r', encoding='utf-8') as fd:
            self.param = fd.read()
            # Get Actual params
            self.param = self.mutation_map #temporary
            
            # Important to print out the syntax of node tree
            # print("\n", dump(self.tree)) ##Used for understanding utilization of ast methods

    def generateMutants(self):
        self.mutants = self.mutator.generateMutations(self.tree, self.param)

    def retNumMutants(self):
        return len(self.mutants)

    def loadMutatedCode(self, i):
        self.converter.loadMutatedCode(self.mutants[i])

    def loadOriginalCode(self):
        self.converter.loadOriginalCode()

    def retOriginalCode(self):
        return self.converter.getOriginalCode()
    


