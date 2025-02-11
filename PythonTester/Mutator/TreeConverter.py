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
        "BitInvert" : NodeType.BINARYOPERATION,
        "Not" : NodeType.NOT,
        "Plus" : NodeType.PLUS,
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
        mTree = MutationTree(self.convertNode(tree))
        return mTree
    
    def unmakeMTree(self, mTree):
        # do conversion back to library tree
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
    
    def convertNode(self, node):
        if (node is None):
            return None
        newType = self.conversion_map.get(type(node).__name__)
        basicOps = [NodeType.ADD, NodeType.ADDASSIGN, 
                    NodeType.SUBTRACT, NodeType.SUBTRACTASSIGN,
                    NodeType.MULTIPLY, NodeType.MULTIPLYASSIGN,
                    NodeType.DIVIDE, NodeType.DIVIDEASSIGN,
                    NodeType.MODULO, NodeType.MODULOASSIGN,
                    NodeType.BITAND, NodeType.BITANDASSIGN,
                    NodeType.BITOR, NodeType.BITORASSIGN,
                    NodeType.POWER,
                    NodeType.LESSTHAN, NodeType.GREATERTHAN, NodeType.EQUAL,
                    NodeType.LESSTHANEQUAL, NodeType.GREATERTHANEQUAL,
                    NodeType.AND, NodeType.OR, NodeType.IS]
        unaryOps = [NodeType.BITINVERT, NodeType.MINUS, NodeType.NOT, NodeType.PLUS]
        rowNumber = self.getRowNumber(node)
        colNumber = self.getColNumber(node)
        dataDict = {}
        if(newType in basicOps):
            wBNode = self.convertNode(node.whitespace_before)
            dataDict['whitespaceBefore'] = wBNode
            wANode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = wANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wBNode, wANode])
        elif(newType == NodeType.NOTEQUAL):
            value = node.value
            wBNode = self.convertNode(node.whitespace_before)
            dataDict['whitespaceBefore'] = wBNode
            wANode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = wANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([wBNode, wANode])
        elif(newType == NodeType.MODULE):
            bNode = self.convertNode(node.body) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['body'] = bNode
            hNode = self.convertNode(node.header) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['header'] = hNode
            fNode = self.convertNode(node.footer) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['footer'] = fNode
            encoding = node.encoding
            dataDict['encoding'] = encoding
            dIndent = node.default_indent
            dataDict['defaultIndent'] = dIndent
            dNewline = node.default_newline
            dataDict['defaultNewline'] = dNewline
            hTNewline = node.has_trailing_newline
            dataDict['hasTrailingNewline'] = hTNewline
            visit = node.visit
            dataDict['visit'] = visit
            cfNode = node.code_for_node
            dataDict['codeForNode'] = cfNode
            docstring = node.get_docstring
            dataDict['getDocstring'] = docstring
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, hNode, fNode])
        elif(newType == NodeType.EMPTYLINE):
            indent = node.indent
            dataDict['indent'] = indent
            wNode = self.convertNode(node.whitespace)
            dataDict['whitespace'] = wNode
            cNode = self.convertNode(node.comment)
            dataDict['comment'] = cNode
            nNode = self.convertNode(node.newline)
            dataDict['newline'] = nNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wNode, cNode, nNode])
        elif(newType == NodeType.SIMPLEWHITESPACE):
            value = node.value
            empty = node.empty
            dataDict['empty'] = empty
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([wNode, cNode, nNode])
        elif(newType == NodeType.COMMENT or NodeType.NEWLINE):
            value = node.value
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
        elif(newType == NodeType.FUNCTIONDEF):
            nameNode = self.convertNode(node.name)
            dataDict['name'] = nameNode
            pNode = self.convertNode(node.params)
            dataDict['params'] = pNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            bNode = self.convertNode(node.decorators) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['decorators'] = bNode
            bNode = self.convertNode(node.returns)
            dataDict['returns'] = bNode
            bNode = self.convertNode(node.asynchronous)
            dataDict['asynchronous'] = bNode
            lLNode = self.convertNode(node.leading_lines) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leadingLines'] = lLNode
            lADNode = self.convertNode(node.lines_after_decorators) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['linesAfterDecorators'] = lADNode
            wADNode = self.convertNode(node.whitespace_after_def)
            dataDict['whitespaceAfterDef'] = wADNode
            wANNode = self.convertNode(node.whitespace_after_name)
            dataDict['whitespaceAfterName'] = wANNode
            wBPNode = self.convertNode(node.whitespace_before_params)
            dataDict['whitespaceBeforeParams'] = wBPNode
            wBCNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wBCNode
            tPNode = self.convertNode(node.type_parameters)
            dataDict['typeParameters'] = tPNode
            wATPNode = self.convertNode(node.whitespace_after_type_parameters)
            dataDict['whitespaceAfterTypeParameters'] = wATPNode
            docstring = node.get_docstring
            dataDict['getDocstring'] = docstring
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([nameNode, pNode, bNode, lLNode, lADNode, wADNode, wANNode, wBPNode, wBCNode, tPNode, wATPNode])
        elif(newType == NodeType.NAME):
            value = node.value
            lNode = self.convertNode(node.lpar)
            dataDict['lpar'] = lNode
            rNode = self.convertNode(node.rpar)
            dataDict['rpar'] = rNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([lNode, rNode])
        elif(newType == NodeType.PARAMETERS):
            pNode = self.convertNode(node.params) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['params'] = pNode
            sANode = self.convertNode(node.star_arg)
            dataDict['starArg'] = sANode
            kPNode = self.convertNode(node.kwonly_params) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['kwonlyParams'] = kPNode
            sKNode = self.convertNode(node.star_kwarg)
            dataDict['starKwarg'] = sKNode
            pPNode = self.convertNode(node.posonly_params) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['posonlyParams'] = pPNode
            pINode = self.convertNode(node.posonly_ind)
            dataDict['posonlyInd'] = pINode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([pNode, sANode, kPNode, sKNode, pPNode, pINode])
        elif(newType == NodeType.INDENTEDBLOCK):
            bNode = self.convertNode(node.body) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['body'] = bNode
            hNode = self.convertNode(node.header)
            dataDict['header'] = hNode
            indent = node.indent
            dataDict['indent'] = indent
            fNode = self.convertNode(node.footer) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['footer'] = fNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, hNode, fNode])
        elif(newType == NodeType.TRAILINGWHITESPACE):
            wNode = self.convertNode(node.whitespace)
            dataDict['whitespace'] = wNode
            cNode = self.convertNode(node.comment)
            dataDict['comment'] = cNode
            nNode = self.convertNode(node.newline)
            dataDict['newline'] = nNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wNode, cNode, nNode])
        elif(newType == NodeType.SIMPLESTATEMENTLINE):
            bNode = self.convertNode(node.body) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['body'] = bNode
            lLNode = self.convertNode(node.leading_lines) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leadingLines'] = lLNode
            tWNode = self.convertNode(node.trailing_whitespace)
            dataDict['trailingWhitespace'] = tWNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, lLNode, tWNode])
        elif(newType == NodeType.EXPR):
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            lLNode = self.convertNode(node.leading_lines)
            dataDict['leadingLines'] = lLNode
            tWNode = self.convertNode(node.trailing_whitespace)
            dataDict['trailingWhitespace'] = tWNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, lLNode, tWNode])
        elif(newType == NodeType.CALL):
            print("hi")
        elif(newType == NodeType.ARG):
            print("hi")
        elif(newType == NodeType.SIMPLESTRING):
            value = node.value
            lparNode = self.convertNode(node.lpar)
            dataDict['leftParenthesis'] = lparNode
            rparNode = self.convertNode(node.rpar)
            dataDict['rightParenthesis'] = rparNode
            dataDict['prefix'] = node.prefix
            dataDict['quote'] = node.quote
            rValue = node.raw_value
            eValue = node.evaluated_value
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([lparNode, rparNode])
        elif(newType == NodeType.RETURN):
            print("hi")
        elif(newType == NodeType.ASSIGN):
            print("hi")
        elif(newType == NodeType.ASSIGNTARGET):                        
            print("hi")
        elif(newType == NodeType.LIST):
            print("hi")
        elif(newType == NodeType.LEFTSQUAREBRACKET or NodeType.LEFTPAREN):
            print("hi")
        elif(newType == NodeType.RIGHTSQUAREBRACKET or NodeType.RIGHTPAREN):
            print("hi")
        elif(newType == NodeType.ELEMENT):
            print("hi") 
        elif(newType == NodeType.INTEGER):
            print("hi")
        elif(newType == NodeType.COMMA):
            print("hi")
        elif(newType == NodeType.BINARYOPERATION):
            print("hi")
        elif(newType == NodeType.FOR):
            print("hi")
            targetNode = self.convertNode(node.target)
            dataDict['target'] = targetNode
            iterNode = self.convertNode(node.iter)
            dataDict['iter'] = iterNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            orElseNode = self.convertNode(node.orelse)
            dataDict['orelse'] = orElseNode
            asyncNode = self.convertNode(node.asynchronous)
            dataDict['asynchronous'] = asyncNode
            leadLineNode = self.convertNode(node.leading_lines)
            dataDict['leadingLines'] = leadLineNode
            wsafNode = self.convertNode(node.whitespace_after_for)
            dataDict['whitespaceAfterFor'] = wsafNode
            wsbiNode = self.convertNode(node.whitespace_before_in)
            dataDict['whitespaceBeforeIn'] = wsbiNode
            wsaiNode = self.convertNode(node.whitespace_after_in)
            dataDict['whitespaceAfterIn'] = wsaiNode
            wsbcNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wsbcNode
        elif(newType == NodeType.AUGASSIGN):    
            print("hi")
        elif(newType == NodeType.UNARYOPERATION):
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            exNode = self.convertNode(node.expression)
            dataDict['expression'] = exNode
            lparNode = self.convertNode(node.lpar)
            dataDict['lpar'] = lparNode
            rparNode = self.convertNode(node.rpar)
            dataDict['rpar'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([opNode, exNode, lparNode, rparNode])
        elif(newType in unaryOps):
            wANode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = wANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wANode])
        elif(newType == NodeType.COMPARISON):
            lNode = self.convertNode(node.left)
            dataDict['left'] = lNode
            compsNode = self.convertNode(node.comparisons) #seq
            dataDict['comparisons'] = compsNode
            lparNode = self.convertNode(node.lpar) #seq
            dataDict['lpar'] = lparNode
            rparNode = self.convertNode(node.rpar) #seq
            dataDict['rpar'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([lNode, compsNode, lparNode, rparNode])
        elif(newType == NodeType.COMPARISONTARGET):
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            compNode = self.convertNode(node.comparator)
            dataDict['comparator'] = compNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([opNode, compNode])
        elif(newType == NodeType.BOOLEANOPERATION):
            lNode = self.convertNode(node.left)
            dataDict['left'] = lNode
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            rNode = self.convertNode(node.right)
            dataDict['right'] = rNode
            lparNode = self.convertNode(node.lpar) #seq
            dataDict['lpar'] = lparNode
            rparNode = self.convertNode(node.rpar) #seq
            dataDict['rpar'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([lNode, opNode, rNode, lparNode, rparNode])
        elif(newType == NodeType.IFEXP):
            testNode = self.convertNode(node.test)
            dataDict['test'] = testNode
            bodyNode = self.convertNode(node.body)
            dataDict['body'] = bodyNode
            orelseNode = self.convertNode(node.orelse)
            dataDict['orelse'] = orelseNode
            lparNode = self.convertNode(node.lpar) #seq
            dataDict['lpar'] = lparNode
            rparNode = self.convertNode(node.rpar) #seq
            dataDict['rpar'] = rparNode
            wBINode = self.convertNode(node.whitespace_before_if)
            dataDict['whitespaceBeforeIf'] = wBINode
            wAINode = self.convertNode(node.whitespace_after_if)
            dataDict['whitespaceAfterIf'] = wAINode
            wBENode = self.convertNode(node.whitespace_before_else)
            dataDict['whitespaceBeforeElse'] = wBENode
            wAENode = self.convertNode(node.whitespace_after_else)
            dataDict['whitespaceAfterElse'] = wAENode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([testNode, bodyNode, orelseNode, lparNode,
                                  rparNode, wBINode, wAINode, wBENode, wAENode])
        with open("test.txt", "a", encoding='utf-8') as f:
            if type(node).__name__ not in self.lst:
                self.lst.append(type(node).__name__)
                f.write(type(node).__name__ + '\n')
                print(str(node.field()) + '\n')
                
        return mNode
    
    def getRowNumber(self, node):
        return 0
    
    def getColNumber(self, node):
        return 0
    
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
    