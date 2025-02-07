import MutationTree
import NodeTypes
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import libcst as cst

PY_LANGUAGE = Language(tspython.language())

tempTree = None

conversion_map = {
    "Add()" : NodeTypes.NodeType.ADD,
    "AddAssign()" : NodeTypes.NodeType.ADDASSIGN,
    "Subtract()" : NodeTypes.NodeType.SUBTRACT,
    "SubtractAssign()" : NodeTypes.NodeType.SUBTRACTASSIGN,
    "Multiply()" : NodeTypes.NodeType.MULTIPLY,
    "MultiplyAssign()" : NodeTypes.NodeType.MULTIPLYASSIGN,
    "Divide()" : NodeTypes.NodeType.DIVIDE,
    "DivideAssign()" : NodeTypes.NodeType.DIVIDEASSIGN,
    "Modulo()" : NodeTypes.NodeType.MODULO,
    "ModuloAssign()" : NodeTypes.NodeType.MODULOASSIGN,
    "BitAnd()": NodeTypes.NodeType.BITAND,
    "BitOr()" : NodeTypes.NodeType.BITOR,
    "Power()" : NodeTypes.NodeType.POWER,
    "LessThan()" : NodeTypes.NodeType.LESSTHAN,
    "GreaterThan()" : NodeTypes.NodeType.GREATERTHAN,
    "Equal()" : NodeTypes.NodeType.EQUAL,
    "NotEqual()" : NodeTypes.NodeType.NOTEQUAL,
    "LessThanEqual()" : NodeTypes.NodeType.LESSTHANEQUAL,
    "GreaterThanEqual()" : NodeTypes.NodeType.GREATERTHANEQUAL,
    "Class()" : NodeTypes.NodeType.CLASS,
    "Method()" : NodeTypes.NodeType.METHOD,
    "Variable()" : NodeTypes.NodeType.VARIABLE, 
    "Assign()" : NodeTypes.NodeType.ASSIGN,
    "Value()" : NodeTypes.NodeType.VALUE,

}

class TreeConverter:
    # parser = Parser(PY_LANGUAGE)
    # treeSitter = None
    originalCode = None
    file = ""
    C = ""
    
    def __init__(self, file_path, C):
        self.file = file_path
        self.C = C
        with open(self.C + self.file, 'r', encoding='utf-8') as fd:
            self.original_code = fd.read()
        fd.close()

        self.metaDataVisitor = None
        self.visitor = VisitNodes()
        

    def getTree(self):
        # newTree = self.parser.parse(self.original_code)
        newTree = cst.parse_module(self.original_code)
        mTree = self.makeMTree(newTree) # Convert to our tree
        return mTree

    def makeMTree(self, tree):
        global tempTree
        tempTree = MutationTree.MutationTree(MutationTree.MutationNode(None, None))
        self.metaDataVisitor = cst.MetadataWrapper(tree)
        self.metaDataVisitor.visit(self.visitor)
        mTree = tempTree
        return mTree
    
    def unmakeMTree(self, mTree):
        #do conversion back to library tree
        newTree = None
        return newTree

    def loadOriginalCode(self):
        # load originalCode
        with open(self.file, 'w', encoding='utf-8') as fd:
            fd.write(self.originalCode)
            fd.flush()
            fd.close()
        return

    def loadMutatedCode(self, mTree):
        newTree = self.unmakeMTree(mTree)
        mutatedCode = self.backToCode(newTree)

        #load mutation
        with open(self.C + self.file, 'w', encoding='utf-8') as fd:
            fd.write(mutatedCode)
            fd.flush()
            fd.close()
            # self.tree = cst.parse_module(self.mutations[i])
        return
    
    def backToCode(self, tree):
        code = None
        return code
    
    def getOriginalCode(self):
        return self.originalCode
    
class VisitNodes(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)
    global tempTree

    def on_visit(self, node):
        # Called every time a node is visited, before we've visited its children.

        # Returns ``True`` if children should be visited, and returns ``False``
        # otherwise.
        print(type(node).__name__)
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if visit_func is not None:
            retval = visit_func(node)
        else:
            retval = True
        # Don't visit children IFF the visit function returned False.
        return False if retval is False else True
    
    def visit_Module(self, node):
        pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start
        # tempTree.currentNode.attachChildren()

    # def visit_BaseExpression(self, node):
    #     pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start

    # def visit_Name(self, node):
    #     pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start
        
    # def visit_Attribute(self, node):
    #     pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start
        
    # def visit_UnaryOperation(self, node):
    #     pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start

    # def visit_BinaryOperation(self, node):
    #     pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start

    # def visit_AugAssign(self, node):
    #     pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start