import os
import yaml
# import libcst as cst

from Mutator.TreeMutator import TreeMutator
from Mutator.TreeConverter import TreeConverter
from Mutator.NodeTypes import NodeType

class MutationGenerator:

    symbol_map = {
        "+" : NodeType.ADD,
        "+=" : NodeType.ADDASSIGN,
        "-" : NodeType.SUBTRACT,
        "-=" : NodeType.SUBTRACTASSIGN,
        "*" : NodeType.MULTIPLY,
        "*=" : NodeType.MULTIPLYASSIGN,
        "/" : NodeType.DIVIDE,
        "/=" : NodeType.DIVIDEASSIGN,
        "%" : NodeType.MODULO,
        "%=" : NodeType.MODULOASSIGN,
        "&" : NodeType.BITAND,
        "|" : NodeType.BITOR,
        # comment the following out for display
        ">" : NodeType.GREATERTHAN,
        ">=" : NodeType.GREATERTHANEQUAL,
        "<" : NodeType.LESSTHAN,
        "<=" : NodeType.LESSTHANEQUAL,
        # this next section to show surviving mutants
        "==" : NodeType.EQUAL,
        "!=" : NodeType.NOTEQUAL,
        "and" : NodeType.AND,
        "And" : NodeType.AND,
        "&&" : NodeType.AND,
        "or" : NodeType.OR,
        "Or" : NodeType.OR,
        "||" : NodeType.OR,
        "if" : NodeType.IF,
        "else" : NodeType.ELSE,
        "True" : NodeType.TRUE,
        "true" : NodeType.TRUE,
        "False" : NodeType.FALSE,
        "false" : NodeType.FALSE,
        "0" : NodeType.INTEGER,
        "1" : NodeType.INTEGER,
        "int" : NodeType.INTEGER,
        "num" : NodeType.INTEGER,
    }

    # mutation_map = {
    #     NodeType.ADD : NodeType.SUBTRACT,
    #     NodeType.ADDASSIGN : NodeType.SUBTRACTASSIGN,
    #     NodeType.SUBTRACT : NodeType.ADD,
    #     NodeType.SUBTRACTASSIGN : NodeType.ADDASSIGN,
    #     NodeType.MULTIPLY : NodeType.DIVIDE,
    #     NodeType.MULTIPLYASSIGN : NodeType.DIVIDEASSIGN,
    #     NodeType.DIVIDE : NodeType.MULTIPLY,
    #     NodeType.DIVIDEASSIGN: NodeType.MULTIPLYASSIGN,
    #     NodeType.MODULO : NodeType.MULTIPLY,
    #     NodeType.MODULOASSIGN : NodeType.MULTIPLYASSIGN,
    #     NodeType.BITAND: NodeType.BITOR,
    #     NodeType.BITOR : NodeType.BITAND,
    #     # comment the following out for display
    #     NodeType.GREATERTHAN : [NodeType.LESSTHAN, NodeType.GREATERTHANEQUAL],
    #     NodeType.GREATERTHANEQUAL : [NodeType.LESSTHAN, NodeType.GREATERTHAN],
    #     NodeType.LESSTHAN : [NodeType.GREATERTHAN, NodeType.LESSTHANEQUAL],
    #     NodeType.LESSTHANEQUAL : [NodeType.GREATERTHAN, NodeType.LESSTHAN],
    #     # this next section to show surviving mutants
    #     NodeType.EQUAL: NodeType.NOTEQUAL,
    #     NodeType.NOTEQUAL : NodeType.EQUAL,
    #     NodeType.AND : NodeType.OR,
    #     NodeType.OR : [NodeType.AND, NodeType.NOTEQUAL],
    #     NodeType.IF : [NodeType.TRUE, NodeType.FALSE],
    #     NodeType.ELSE : [NodeType.TRUE, NodeType.FALSE],
    #     NodeType.INTEGER : NodeType.INTEGER
    # }

    C = ""
    # mutant_path = ""
    config_path = ""

    converter = None
    tree = None
    mutants = []
    mutantNodes = []
    mutantTypes = []
    mutationObjects = []

    mutator = None
    param = ""
    
    def __init__(self, fs, config):
        # global tree, og_tree
        # VERY IMPORTANT STEP!!!!!
        # Establish path to original file
        self.C = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        
        self.converter = TreeConverter(fs, self.C)
        self.tree = self.converter.getTree()

        self.mutator = TreeMutator()
        self.config_path = config
        self.file_path = fs

        with open(self.config_path, 'r', encoding='utf-8') as fd:
            mapLocation = yaml.safe_load(fd)['mutation_map']
            fd.close()

        with open(self.C + "\\" + mapLocation, 'r', encoding='utf-8') as md:
            mutation_map = {}
            for line in md:
                mList = []
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    vList = value.strip().split(',')
                    for item in vList:
                        mList.append(self.symbol_map[str(item.strip())])
                    mutation_map[self.symbol_map[str(key.strip())].value] = mList

            self.param = mutation_map
            
            # Important to print out the syntax of node tree
            # print("\n", dump(self.tree)) ##Used for understanding utilization of ast methods

    def generateMutants(self):
        mutant = self.mutator.generateMutations(self.tree, self.param)
        while(mutant is not None):
            self.mutants.append(self.converter.unmakeMTree(mutant))
            self.mutantNodes.append(mutant.retCurNode().toString())
            self.mutantTypes.append(mutant.retCurNode().nodeType.name)
            self.mutationObjects.append(mutant.retCurNode().method_name)
            mutant = self.mutator.generateMutations(self.tree, self.param)
            

    def retNumMutants(self):
        return len(self.mutants)
    
    def retMutations(self):
        return self.mutants

    def loadMutatedCode(self, i):
        self.converter.loadMutatedCode(self.mutants[i])


    def loadOriginalCode(self):
        self.converter.loadOriginalCode()

    def retOriginalCode(self):
        return self.converter.getOriginalCode()
    


