import os
import yaml
from pathlib import Path
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
        self.C = Path(__file__).resolve().parent.parent          # .../PythonTester
        self.config_path = Path(config).resolve()

        # Normalize file path (absolute)
        fs_path = Path(fs)
        if not fs_path.is_absolute():
            fs_path = (self.C / fs_path).resolve()
        self.file_path = str(fs_path)

        # Set up converter/tree
        self.converter = TreeConverter(self.file_path, str(self.C))
        self.tree = self.converter.getTree()

        self.mutator = TreeMutator()

        # Read map location from config (with sane defaults)
        with self.config_path.open('r', encoding='utf-8') as fd:
            cfg = yaml.safe_load(fd) or {}
        map_location = cfg.get('mutation_map', 'mutationMap.txt')

        # Allow env override (useful from MCP / CI)
        map_override = os.environ.get("MUTATION_MAP")
        if map_override:
            map_path = Path(map_override)
        else:
            mp = Path(map_location)
            map_path = mp if mp.is_absolute() else (self.C / mp)

        map_path = map_path.resolve()

        if not map_path.exists():
            raise FileNotFoundError(
                f"mutationMap not found at: {map_path}\n"
                f"Hint: ensure the file exists (case-sensitive on Linux) or set MUTATION_MAP=/abs/path/mutationMap.txt"
            )

        # Parse mutation map file
        mutation_map = {}
        with map_path.open('r', encoding='utf-8') as md:
            for line in md:
                if ':' not in line:
                    continue
                key, value = line.strip().split(':', 1)
                variants = [v.strip() for v in value.strip().split(',') if v.strip()]
                # Map symbol strings -> NodeType values, store as list
                try:
                    k_node = self.symbol_map[str(key.strip())].value
                    v_nodes = [self.symbol_map[s].value for s in variants]
                    mutation_map[k_node] = v_nodes
                except KeyError as e:
                    raise KeyError(f"Unknown symbol in mutationMap.txt: {e} (line: {line.strip()})")

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
    


