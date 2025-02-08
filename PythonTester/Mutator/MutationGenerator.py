import os
import libcst as cst

from Mutator import TreeMutator
from Mutator import MutationTree
from Mutator import TreeConverter
from Mutator import NodeTypes

class MutationGenerator:

    mutation_map = {
        NodeTypes.NodeType.ADD : NodeTypes.NodeType.SUBTRACT,
        NodeTypes.NodeType.ADDASSIGN : NodeTypes.NodeType.SUBTRACTASSIGN,
        NodeTypes.NodeType.SUBTRACT : NodeTypes.NodeType.ADD,
        NodeTypes.NodeType.SUBTRACTASSIGN : NodeTypes.NodeType.ADDASSIGN,
        NodeTypes.NodeType.MULTIPLY : NodeTypes.NodeType.DIVIDE,
        NodeTypes.NodeType.MULTIPLYASSIGN : NodeTypes.NodeType.DIVIDEASSIGN,
        NodeTypes.NodeType.DIVIDE : NodeTypes.NodeType.MULTIPLY,
        NodeTypes.NodeType.DIVIDEASSIGN: NodeTypes.NodeType.MULTIPLYASSIGN,
        NodeTypes.NodeType.MODULO : NodeTypes.NodeType.MULTIPLY,
        NodeTypes.NodeType.MODULOASSIGN : NodeTypes.NodeType.MULTIPLYASSIGN,
        NodeTypes.NodeType.BITAND: NodeTypes.NodeType.BITOR,
        NodeTypes.NodeType.BITOR : NodeTypes.NodeType.BITAND,
    }

    C = ""
    # mutatant_path = ""
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
        
        self.converter = TreeConverter.TreeConverter(fs, self.C)
        self.tree = self.converter.getTree()

        self.mutator = TreeMutator.TreeMutator()
        self.config_path = config

        with open(self.C + self.config_path, 'r', encoding='utf-8') as fd:
            self.param = fd.read()
            # Get Actual params
            self.param = self.mutation_map #temporary
            # self.mutants = self.mutator.generateMutations(self.tree, self.param)
            
            # Important to print out the syntax of node tree
            # print("\n", dump(self.tree)) ##Used for understanding utilization of ast methods


    def loadMutatedCode(self, i):
        self.converter.loadMutatedCode(self.mutants[i])

    def loadOriginalCode(self):
        self.converter.loadOriginalCode()

    def retOriginalCode(self):
        return self.converter.getOriginalCode()
    


