from Mutator.MutationTree import MutationTree
from Mutator.MutationTree import MutationNode
from Mutator.NodeTypes import NodeType
# import tree_sitter_python as tspython
# from tree_sitter import Language, Parser
import libcst as cst

# PY_LANGUAGE = Language(tspython.language())
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
        "SimpleWhitespace" : NodeType.SIMPLEWHITESPACE,
        "Comment" : NodeType.COMMENT,
        "Newline" : NodeType.NEWLINE,
        "FunctionDef" : NodeType.FUNCTIONDEF,
        "Name" : NodeType.NAME,
        "Parameters" : NodeType.PARAMETERS,
        "IndentedBlock" : NodeType.INDENTEDBLOCK,
        "TrailingWhitespace" : NodeType.TRAILINGWHITESPACE,
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
        "LeftParen" : NodeType.LEFTPAREN,
        "And" : NodeType.AND,
        "RightParen" : NodeType.RIGHTPAREN,
        "Or" : NodeType.OR,
        "IfExp" : NodeType.IFEXP,
        "Is" : NodeType.IS,
        "BitInvert" : NodeType.BINARYOPERATION,
        "Not" : NodeType.NOT,
        "Plus" : NodeType.PLUS,
        "MaybeSentinel" : NodeType.MAYBESENTINEL,
        "ClassDef" : NodeType.CLASSDEF,
        "Param" : NodeType.PARAM,
        "ParamStar" : NodeType.PARAMSTAR,
        "AssignEqual" : NodeType.ASSIGNEQUAL,
        "BaseExpression" : NodeType.BASEEXPRESSION,
        "Annotation" : NodeType.ANNOTATION,
        "BaseParenthesizableWhitespace" : NodeType.BASEPARENTHESIZABLEWHITESPACE,
        "Semicolon" : NodeType.SEMICOLON,
        "BaseCompoundStatement" : NodeType.BASECOMPOUNDSTATEMENT,
    }

    # parser = Parser(PY_LANGUAGE)
    # treeSitter = None
    original_code = None
    file = ""
    C = ""
    
    def __init__(self, file_path, C):
        self.file = file_path
        self.C = C
        with open(self.C + self.file, 'r', encoding='utf-8') as fd:
            self.original_code = fd.read()
        fd.close()

        print('OG file dest: ' + self.C + self.file + '\n') #debug

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
        with open(self.C + self.file, 'w', encoding='utf-8') as fd:
            fd.write(self.original_code)
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
        return self.original_code
    
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
                    NodeType.POWER, NodeType.COMMA,
                    NodeType.LESSTHAN, NodeType.GREATERTHAN, NodeType.EQUAL,
                    NodeType.LESSTHANEQUAL, NodeType.GREATERTHANEQUAL,
                    NodeType.AND, NodeType.OR, NodeType.IS, NodeType.ASSIGNEQUAL, 
                    NodeType.SEMICOLON]
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
            bNode = []
            for n in node.body:
                bNodeChild = self.convertNode(n)
                bNode.append(bNodeChild) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['body'] = bNode
            hNode = []
            for n in node.header:
                hNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['header'] = hNode
            fNode = []
            for n in node.footer:
                fNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['footer'] = fNode
            encoding = node.encoding
            dataDict['encoding'] = encoding
            dIndent = node.default_indent
            dataDict['defaultIndent'] = dIndent
            dNewline = node.default_newline
            dataDict['defaultNewline'] = dNewline
            hTNewline = node.has_trailing_newline
            dataDict['hasTrailingNewline'] = hTNewline
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, hNode, fNode])
        elif(newType == NodeType.EMPTYLINE):
            indent = node.indent
            dataDict['indent'] = indent
            wNode = self.convertNode(node.whitespace) 
            dataDict['whitespace'] = wNode
            if(hasattr(node, 'comment')):
                cNode = self.convertNode(node.comment) # Can be None
            else:
                cNode = None
            dataDict['comment'] = cNode
            nNode = self.convertNode(node.newline)
            dataDict['newline'] = nNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wNode, cNode, nNode])
        elif(newType == NodeType.SIMPLEWHITESPACE):
            value = node.value
            empty = node.empty # Is a property. 
            dataDict['empty'] = empty
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
        elif(newType == NodeType.COMMENT or newType == NodeType.NEWLINE):
            if(hasattr(node, 'value')):
                value = node.value # Can be None.
            else:
                value = None
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
        elif(newType == NodeType.FUNCTIONDEF):
            nameNode = self.convertNode(node.name)
            dataDict['name'] = nameNode
            pNode = self.convertNode(node.params)
            dataDict['params'] = pNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            dNode = []
            for n in node.decorators:
                dNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['decorators'] = dNode
            if(hasattr(node, 'returns')):
                rNode = self.convertNode(node.returns) # Can be None
            else:
                rNode = None
            dataDict['returns'] = rNode
            if(hasattr(node, 'asynchronous')):
                aNode = self.convertNode(node.asynchronous) # Can be None
            else:
                aNode = None
            dataDict['asynchronous'] = aNode
            lLNode = []
            for n in node.leading_lines:
                self.convertNode(n) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leadingLines'] = lLNode
            lADNode = []
            for n in node.lines_after_decorators:
                self.convertNode(n) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['linesAfterDecorators'] = lADNode
            wADNode = self.convertNode(node.whitespace_after_def)
            dataDict['whitespaceAfterDef'] = wADNode
            wANNode = self.convertNode(node.whitespace_after_name)
            dataDict['whitespaceAfterName'] = wANNode
            wBPNode = self.convertNode(node.whitespace_before_params)
            dataDict['whitespaceBeforeParams'] = wBPNode
            wBCNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wBCNode
            if(hasattr(node, 'type_parameters')):
                tPNode = self.convertNode(node.type_parameters) # Can be None
            else:
                tPNode = None
            dataDict['typeParameters'] = tPNode
            wATPNode = self.convertNode(node.whitespace_after_type_parameters)
            dataDict['whitespaceAfterTypeParameters'] = wATPNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([nameNode, pNode, bNode, dNode, rNode, aNode, lLNode, lADNode, wADNode, wANNode, wBPNode, wBCNode, tPNode, wATPNode])
        elif(newType == NodeType.NAME):
            value = node.value
            lNode = []
            for n in node.lpar:
                lNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['lpar'] = lNode
            rNode = []
            for n in node.rpar:
                rNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rpar'] = rNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([lNode, rNode])
        elif(newType == NodeType.PARAMETERS):
            pNode = []
            for n in node.params:
                pNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['params'] = pNode
            sANode = self.convertNode(node.star_arg)
            dataDict['starArg'] = sANode
            kPNode = []
            for n in node.kwonly_params:
                kPNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['kwonlyParams'] = kPNode
            if(hasattr(node, 'star_kwarg')):
                sKNode = self.convertNode(node.star_kwarg) # Can be None
            else:
                sKNode = None
            dataDict['starKwarg'] = sKNode
            pPNode = []
            for n in node.posonly_params:
                pPNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['posonlyParams'] = pPNode
            pINode = self.convertNode(node.posonly_ind)
            dataDict['posonlyInd'] = pINode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([pNode, sANode, kPNode, sKNode, pPNode, pINode])
        elif(newType == NodeType.INDENTEDBLOCK):
            bNode = []
            for n in node.body:
                bNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['body'] = bNode
            hNode = self.convertNode(node.header)
            dataDict['header'] = hNode
            if(hasattr(node, 'indent')):
                indent = node.indent # Can be None
            else:
                indent = None
            dataDict['indent'] = indent
            fNode = []
            for n in node.footer:
                fNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['footer'] = fNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, hNode, fNode])
        elif(newType == NodeType.TRAILINGWHITESPACE):
            wNode = self.convertNode(node.whitespace)
            dataDict['whitespace'] = wNode
            if(hasattr(node, 'comment')):
                cNode = self.convertNode(node.comment) # Can be None. Default set to None
            else:
                cNode = None
            dataDict['comment'] = cNode
            nNode = self.convertNode(node.newline)
            dataDict['newline'] = nNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wNode, cNode, nNode])
        elif(newType == NodeType.SIMPLESTATEMENTLINE):
            bNode = []
            for n in node.body:
                bNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['body'] = bNode
            lLNode = []
            for n in node.leading_lines:
                lLNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leadingLines'] = lLNode
            tWNode = self.convertNode(node.trailing_whitespace)
            dataDict['trailingWhitespace'] = tWNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, lLNode, tWNode])
        elif(newType == NodeType.EXPR):
            value = node.value
            semicolon = self.convertNode(node.semicolon)
            dataDict['semicolon'] = semicolon
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([semicolon])
        elif(newType == NodeType.CALL):
            fNode = self.convertNode(node.func)
            dataDict['func'] = fNode
            aNode = []
            for n in node.args:
                aNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['args'] = aNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode 
            wafNode = self.convertNode(node.whitespace_after_func)
            dataDict['whitespaceAfterFunc'] = wafNode
            wbaNode = self.convertNode(node.whitespace_before_args)
            dataDict['whitespaceBeforeArgs'] = wbaNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([fNode, aNode, lparNode, rparNode, wafNode, wbaNode])
        elif(newType == NodeType.ARG):
            valueNode = self.convertNode(node.value)
            dataDict['value'] = valueNode
            if(hasattr(node, 'keyword')):
                keywordNode = self.convertNode(node.keyword) # Can be None.
            else:
                keywordNode = None
            dataDict['keyword'] = keywordNode
            equalNode = self.convertNode(node.equal)
            dataDict['equal'] = equalNode
            commaNode = self.convertNode(node.comma)
            dataDict['comma'] = commaNode
            star = node.star
            dataDict['star'] = star
            wasNode = self.convertNode(node.whitespace_after_star)
            dataDict['whitespaceAfterStar'] = wasNode
            waaNode = self.convertNode(node.whitespace_after_arg)
            dataDict['whitespaceAfterArg'] = waaNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([valueNode, keywordNode, equalNode, commaNode, wasNode, waaNode])
        elif(newType == NodeType.SIMPLESTRING):
            value = node.value
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode 
            dataDict['prefix'] = node.prefix
            dataDict['quote'] = node.quote
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([lparNode, rparNode])
        elif(newType == NodeType.RETURN):
            if(hasattr(node, 'value')):
                vNode = self.convertNode(node.value) # Can be None.
            else:
                vNode = None
            dataDict['value'] = vNode
            warNode = self.convertNode(node.whitespace_after_return)
            dataDict['whitespaceAfterReturn'] = warNode
            sNode = self.convertNode(node.semicolon)
            dataDict['semicolon'] = sNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([vNode, warNode, sNode])
        elif(newType == NodeType.ASSIGN):
            tNode = []
            for n in node.targets:
                tNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['targets'] = tNode
            vNode = self.convertNode(node.value)
            dataDict['value'] = vNode
            sNode = self.convertNode(node.semicolon) # could be MaybeSentinel, need to handle
            dataDict['semicolon'] = sNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([tNode, vNode, sNode])
        elif(newType == NodeType.ASSIGNTARGET):                        
            tNode = self.convertNode(node.target)
            dataDict['target'] = tNode
            wbeNode = self.convertNode(node.whitespace_before_equal)
            dataDict['whitespaceBeforeEqual'] = wbeNode
            waeNode = self.convertNode(node.whitespace_after_equal)
            dataDict['whitespaceAfterEqual'] = waeNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([tNode, wbeNode, waeNode])
        elif(newType == NodeType.LIST):
            eNode = []
            for n in node.elements:
                eNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['elements'] = eNode
            lbNode = self.convertNode(node.lbracket)
            dataDict['leftBracket'] = lbNode
            rbNode = self.convertNode(node.rbracket)
            dataDict['rightBracket'] = rbNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([eNode, lbNode, rbNode, lparNode, rparNode])
        elif(newType == NodeType.LEFTSQUAREBRACKET or newType == NodeType.LEFTPAREN):
            waNode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = waNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([waNode])
        elif(newType == NodeType.RIGHTSQUAREBRACKET or newType == NodeType.RIGHTPAREN):
            wbNode = self.convertNode(node.whitespace_before)
            dataDict['whitespaceBefore'] = wbNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wbNode])
        elif(newType == NodeType.ELEMENT):
            vNode = self.convertNode(node.value)
            dataDict['value'] = vNode
            cNode = self.convertNode(node.comma) # could be MaybeSentinel, need to handle
            dataDict['comma'] = cNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([vNode, cNode])
        elif(newType == NodeType.INTEGER):
            value = node.value
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
            mNode.attachChildren([lparNode, rparNode])
        elif(newType == NodeType.BINARYOPERATION):
            lNode = self.convertNode(node.left)
            dataDict['left'] = lNode
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            rNode = self.convertNode(node.right)
            dataDict['right'] = rNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([lNode, opNode, rNode, lparNode, rparNode])
        elif(newType == NodeType.FOR):
            targetNode = self.convertNode(node.target)
            dataDict['target'] = targetNode
            iterNode = self.convertNode(node.iter)
            dataDict['iter'] = iterNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            if(hasattr(node, "orelse")):
                orElseNode = self.convertNode(node.orelse) # could be None
            else:
                orElseNode = None
            dataDict['orelse'] = orElseNode
            if(hasattr(node, "asynchronous")):
                asyncNode = self.convertNode(node.asynchronous) # could be None
            else:
                asyncNode = None
            dataDict['asynchronous'] = asyncNode
            leadLineNode = []
            for n in node.leading_lines:
                leadLineNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
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
            tNode = self.convertNode(node.target)
            dataDict['target'] = tNode
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            vNode = self.convertNode(node.value)
            dataDict['value'] = vNode
            scNode = self.convertNode(node.semicolon) # could be a MaybeSentinel, need to handle
            dataDict['semicolon'] = scNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([tNode, opNode, vNode, scNode])
        elif(newType == NodeType.UNARYOPERATION):
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            exNode = self.convertNode(node.expression)
            dataDict['expression'] = exNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['lpar'] = lparNode
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
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
            compsNode = []
            for n in node.comparisons:
                compsNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['comparisons'] = compsNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
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
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([lNode, opNode, rNode, lparNode, rparNode])
        elif(newType == NodeType.IFEXP):
            testNode = self.convertNode(node.test)
            dataDict['test'] = testNode
            bodyNode = self.convertNode(node.body)
            dataDict['body'] = bodyNode
            orelseNode = self.convertNode(node.orelse)
            dataDict['orelse'] = orelseNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
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
        elif(newType == NodeType.CLASSDEF):
            nameNode = self.convertNode(node.name)
            dataDict['name'] = nameNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            baseNode = []
            for n in node.bases:
                baseNode.append(self.convertNode(n))
            dataDict['bases'] = baseNode
            dNode = []
            for n in node.decorators:
                dNode.append(self.convertNode(n))
            dataDict['decorators'] = dNode
            kNode = []
            for n in node.keywords:
                kNode.append(self.convertNode(n))
            dataDict['keywords'] = kNode
            lparNode = self.convertNode(node.lpar)
            dataDict['leftParenthesis'] = lparNode
            rparNode = self.convertNode(node.rpar)
            dataDict['rightParenthesis'] = rparNode
            llNode = []
            for n in node.leading_lines:
                llNode.append(self.convertNode(n))
            dataDict['leadingLines'] = llNode
            lADNode = []
            for n in node.lines_after_decorators:
                lADNode.append(self.convertNode(n))
            dataDict['linesAfterDecorators'] = lADNode
            wAClassNode = self.convertNode(node.whitespace_after_class)
            dataDict['whitespaceAfterClass'] = wAClassNode
            wANode = self.convertNode(node.whitespace_after_name)
            dataDict['whitespaceAfterName'] = wANode
            wAColonNode = self.convertNode(node.whitespace_after_colon)
            dataDict['whitespaceAfterColon'] = wAColonNode
            if(hasattr(node, 'type_parameters')):
                tPNode = self.convertNode(node.type_parameters)
            else:
                tPNode = None
            dataDict['typeParameters'] = tPNode
            wATPNode = self.convertNode(node.whitespace_after_type_parameters)
            dataDict['whitespaceAfterTypeParameters'] = wATPNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([nameNode, bNode, baseNode, dNode, kNode,
                                  lparNode, rparNode, llNode, lADNode,
                                  wAClassNode, wANode, wAColonNode,
                                  tPNode, wATPNode])
        elif(newType == NodeType.PARAM):
            nNode = node.name
            dataDict['name'] = nNode
            if(hasattr(node, 'annotation')):
                aNode = self.convertNode(node.annotation)
            else:
                aNode = None
            dataDict['annotation'] = aNode
            eNode = self.convertNode(node.equal)
            dataDict['equal'] = eNode
            if(hasattr(node, 'default')):
                dNode = self.convertNode(node.default)
            else: 
                dNode = None
            dataDict['default'] = dNode
            cNode = self.convertNode(node.comma)
            dataDict['comma'] = cNode
            if(isinstance(node.star, str)):
                sNode = node.star
            else:
                sNode = self.convertNode(node.star)
            dataDict['star'] = sNode
            wASNode = self.convertNode(node.whitespace_after_star)
            dataDict['whitespaceAfterStar'] = wASNode
            wAPNode = self.convertNode(node.whitespace_after_param)
            dataDict['whitespaceAfterParam'] = wAPNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([aNode, eNode, dNode, cNode, sNode, wASNode, wAPNode])
        elif(newType == NodeType.PARAMSTAR):
            cNode = self.convertNode(node.comma)
            dataDict['comma'] = cNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([cNode])
        elif(newType == NodeType.ANNOTATION):
            aNode = self.convertNode(node.annotation)
            dataDict['annotation'] = aNode
            wBINode = self.convertNode(node.whitespace_before_indicator)
            dataDict['whitespaceBeforeIndicator'] = wBINode
            wAINode = self.convertNode(node.whitespace_after_indicator)
            dataDict['whitespaceAfterIndicator'] = wAINode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([aNode, wBINode, wAINode])
        elif(newType == NodeType.MAYBESENTINEL or newType == NodeType.BASEEXPRESSION or newType == NodeType.BASEPARENTHESIZABLEWHITESPACE):
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
        with open("test.txt", "a", encoding='utf-8') as f:
            if type(node).__name__ not in self.lst:
                self.lst.append(type(node).__name__)
                f.write(type(node).__name__ + '\n')
                # print(str(node.field()) + '\n')
                
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
    