from Mutator.MutationTree import MutationTree
from Mutator.MutationTree import MutationNode
from Mutator.NodeTypes import NodeType
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import libcst as cst

PY_LANGUAGE = Language(tspython.language())
lst = []

class TreeConverter:
    lst = []

    conversion_map = {
        "Add" : NodeType.ADD,
        "AddAssign" : NodeType.ADDASSIGN,
        "Subtract" : NodeType.SUBTRACT,
        "SubtractAssign" : NodeType.SUBTRACTASSIGN,
        "Multiply" : NodeType.MULTIPLY,
        "MultiplyAssign" : NodeType.MULTIPLYASSIGN,
        "Divide" : NodeType.DIVIDE,
        "DivideAssign" : NodeType.DIVIDEASSIGN,
        "Modulo" : NodeType.MODULO,
        "ModuloAssign" : NodeType.MODULOASSIGN,
        "BitAnd": NodeType.BITAND,
        "BitOr" : NodeType.BITOR,
        "Power" : NodeType.POWER,
        "LessThan" : NodeType.LESSTHAN,
        "GreaterThan" : NodeType.GREATERTHAN,
        "Equal" : NodeType.EQUAL,
        "NotEqual" : NodeType.NOTEQUAL,
        "LessThanEqual" : NodeType.LESSTHANEQUAL,
        "GreaterThanEqual" : NodeType.GREATERTHANEQUAL,
        "Module" : NodeType.MODULE,
        "EmptyLine" : NodeType.EMPTYLINE,
        "SimpleWhiteSpace" : NodeType.SIMPLEWHITESPACE,
        "Comment" : NodeType.COMMENT,
        "NewLine" : NodeType.NEWLINE,
        "FunctionDef" : NodeType.FUNCTIONDEF,
        "Name" : NodeType.NAME,
        "Parameters" : NodeType.PARAMETERS,
        "IndentBlock" : NodeType.INDENTEDBLOCK,
        "TrailingWhiteSpace" : NodeType.TRAILINGWHITESPACE,
        "SimpleStatementLine" : NodeType.SIMPLESTATEMENTLINE,
        "Expr" : NodeType.EXPR,
        "Call" : NodeType.CALL,
        "Arg" : NodeType.ARG,
        "SimpleString" : NodeType.SIMPLESTRING,
        "Return" : NodeType.RETURN,
        "Assign" : NodeType.ASSIGN,
        "AssignTarget" : NodeType.ASSIGNTARGET,
        "List" : NodeType.LIST,
        "LeftSquareBracket" : NodeType.LEFTSQUAREBRACKET,
        "Element" : NodeType.ELEMENT,
        "Integer" : NodeType.INTEGER,
        "Comma" : NodeType.COMMA,
        "RightSquareBracket" : NodeType.RIGHTSQUAREBRACKET,
        "BinaryOperation" : NodeType.BINARYOPERATION,
        "For" : NodeType.FOR,
        "AugAssign" : NodeType.AUGASSIGN,
        "UnaryOperation" : NodeType.UNARYOPERATION,
        "Minus" : NodeType.MINUS,
        "Comparison" : NodeType.COMPARISON,
        "ComparisonTarget" : NodeType.COMPARISONTARGET,
        "BooleanOperation" : NodeType.BOOLEANOPERATION,
        "LeftParne" : NodeType.LEFTPAREN,
        "And" : NodeType.AND,
        "RightParen" : NodeType.RIGHTPAREN,
        "Or" : NodeType.OR,
        "IfExp" : NodeType.IFEXP,
        "Is" : NodeType.IS,
    }

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
        # global tempMTree
        # tempMTree = MutationTree.MutationTree(MutationTree.MutationNode(None, None))
        # self.metaDataVisitor = cst.MetadataWrapper(tree)
        # self.metaDataVisitor.visit(self.visitor)
        # mTree = tempMTree
        mTree = MutationTree(self.traverser(tree))
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
    
    def traverser(self, node):
        mNode = self.convertNode(node)

        for child in node.children:
            mNode.attachChildren(self.traverser(child))
        
        return mNode
    
    def convertNode(self, node):
        newType = self.conversion_map.get(type(node).__name__)
        with open("test.txt", "a", encoding='utf-8') as f:
            if type(node).__name__ not in self.lst:
                self.lst.append(type(node).__name__)
                f.write(type(node).__name__ + '\n')
                print(str(node.field()) + '\n')
                
        mNode = MutationNode(newType)
        return mNode
    
class VisitNodes(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)
    global lst

    def on_visit(self, node):
        # Called every time a node is visited, before we've visited its children.

        # Returns ``True`` if children should be visited, and returns ``False``
        # otherwise

        with open("test.txt", "a", encoding='utf-8') as f:
            if type(node).__name__ not in lst:
                print(lst)
                lst.append(type(node).__name__)
                f.write(type(node).__name__ + '\n')
            # f.write(type(node).__name__ + '\n')
            # print(type(node).__name__)
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if visit_func is not None:
            retval = visit_func(node)
        else:
            retval = True
        # Don't visit children IFF the visit function returned False.
        return False if retval is False else True
    