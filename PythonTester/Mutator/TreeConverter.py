from Mutator.MutationTree import MutationTree
from Mutator.MutationTree import MutationNode
from Mutator.NodeTypes import NodeType
# import tree_sitter_python as tspython
# from tree_sitter import Language, Parser
import libcst as cst
from libcst.metadata import PositionProvider, MetadataWrapper

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
        "BitInvert" : NodeType.BITINVERT,
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
    
    unconversion_map = {
        NodeType.ADD : "Add",
        NodeType.ADDASSIGN : "AddAssign",
        NodeType.SUBTRACT : "Subtract",
        NodeType.SUBTRACTASSIGN : "SubtractAssign",
        NodeType.MULTIPLY : "Multiply",
        NodeType.MULTIPLYASSIGN : "MultiplyAssign",
        NodeType.DIVIDE : "Divide",
        NodeType.DIVIDEASSIGN : "DivideAssign",
        NodeType.MODULO : "Modulo",
        NodeType.MODULOASSIGN : "ModuloAssign",
        NodeType.BITAND : "BitAnd",
        NodeType.BITOR : "BitOr",
        NodeType.POWER : "Power",
        NodeType.LESSTHAN : "LessThan",
        NodeType.GREATERTHAN : "GreaterThan",
        NodeType.EQUAL : "Equal",
        NodeType.NOTEQUAL : "NotEqual",
        NodeType.LESSTHANEQUAL : "LessThanEqual",
        NodeType.GREATERTHANEQUAL : "GreaterThanEqual",
        NodeType.MODULE : "Module",
        NodeType.EMPTYLINE : "EmptyLine",
        NodeType.SIMPLEWHITESPACE : "SimpleWhitespace",
        NodeType.COMMENT : "Comment",
        NodeType.NEWLINE : "Newline",
        NodeType.FUNCTIONDEF : "FunctionDef",
        NodeType.NAME : "Name",
        NodeType.PARAMETERS : "Parameters",
        NodeType.INDENTEDBLOCK : "IndentedBlock",
        NodeType.TRAILINGWHITESPACE : "TrailingWhitespace",
        NodeType.SIMPLESTATEMENTLINE : "SimpleStatementLine",
        NodeType.EXPR : "Expr",
        NodeType.CALL : "Call",
        NodeType.ARG : "Arg",
        NodeType.SIMPLESTRING : "SimpleString",
        NodeType.RETURN : "Return",
        NodeType.ASSIGN : "Assign",
        NodeType.ASSIGNTARGET : "AssignTarget",
        NodeType.LIST : "List",
        NodeType.LEFTSQUAREBRACKET : "LeftSquareBracket",
        NodeType.ELEMENT : "Element",
        NodeType.INTEGER : "Integer",
        NodeType.COMMA : "Comma",
        NodeType.RIGHTSQUAREBRACKET : "RightSquareBracket",
        NodeType.BINARYOPERATION : "BinaryOperation",
        NodeType.FOR : "For",
        NodeType.AUGASSIGN : "AugAssign",
        NodeType.UNARYOPERATION : "UnaryOperation",
        NodeType.MINUS : "Minus",
        NodeType.COMPARISON : "Comparison",
        NodeType.COMPARISONTARGET : "ComparisonTarget",
        NodeType.BOOLEANOPERATION : "BooleanOperation",
        NodeType.LEFTPAREN : "LeftParen",
        NodeType.AND : "And",
        NodeType.RIGHTPAREN : "RightParen",
        NodeType.OR : "Or",
        NodeType.IFEXP : "IfExp",
        NodeType.IS : "Is",
        NodeType.BITINVERT : "BitInvert",
        NodeType.NOT : "Not",
        NodeType.PLUS : "Plus",
        NodeType.MAYBESENTINEL : "MaybeSentinel",
        NodeType.CLASSDEF : "ClassDef",
        NodeType.PARAM : "Param",
        NodeType.PARAMSTAR : "ParamStar",
        NodeType.ASSIGNEQUAL : "AssignEqual",
        NodeType.BASEEXPRESSION : "BaseExpression",
        NodeType.ANNOTATION : "Annotation",
        NodeType.BASEPARENTHESIZABLEWHITESPACE : "BaseParenthesizableWhitespace",
        NodeType.SEMICOLON : "Semicolon",
        NodeType.BASECOMPOUNDSTATEMENT : "BaseCompoundStatement",
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

        # self.metaDataVisitor = None
        # self.visitor = VisitNodes()
        

    def getTree(self):
        # newTree = self.parser.parse(self.original_code)
        wrapper = cst.MetadataWrapper(cst.parse_module(self.original_code))
        self.metadata = wrapper.resolve(PositionProvider)
        module_with_metadata = wrapper.module
        # newTree = cst.parse_module(self.original_code)
        mTree = self.makeMTree(module_with_metadata) # Convert to our tree
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
        headNode = self.unconvertNode(mTree.headNode)
        return headNode

    def loadOriginalCode(self):
        # load originalCode
        with open(self.C + self.file, 'w', encoding='utf-8') as fd:
            fd.write(self.original_code)
            fd.flush()
            fd.close()
        return

    def loadMutatedCode(self, mTree):
        mutatedCode = self.backToCode(mTree)

        #load mutation
        with open(self.C + self.file, 'w', encoding='utf-8') as fd:
            fd.write(mutatedCode)
            fd.flush()
            fd.close()
            # self.tree = cst.parse_module(self.mutations[i])
        return
    
    def backToCode(self, headNode):
        code = headNode.code
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
            
            # Add code property for module node?

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
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
        elif(newType == NodeType.COMMENT or newType == NodeType.NEWLINE):
            if(hasattr(node, 'value')):
                value = node.value # Can be None.
            else:
                value = None
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=value)
        elif(newType == NodeType.FUNCTIONDEF):
            nNode = self.convertNode(node.name)
            dataDict['name'] = nNode
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
                lLNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leadingLines'] = lLNode
            lADNode = []
            for n in node.lines_after_decorators:
                lADNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
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
            mNode.attachChildren([nNode, pNode, bNode, dNode, rNode, aNode, lLNode, lADNode, wADNode, wANNode, wBPNode, wBCNode, tPNode, wATPNode])
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
            sNode = self.convertNode(node.semicolon)
            dataDict['semicolon'] = sNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value = value)
            mNode.attachChildren([sNode])
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
            wAFNode = self.convertNode(node.whitespace_after_func)
            dataDict['whitespaceAfterFunc'] = wAFNode
            wBANode = self.convertNode(node.whitespace_before_args)
            dataDict['whitespaceBeforeArgs'] = wBANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([fNode, aNode, lparNode, rparNode, wAFNode, wBANode])
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
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([targetNode, iterNode, bNode, orElseNode, asyncNode, leadLineNode, wsafNode, wsbiNode, wsaiNode, wsbcNode])
        elif(newType == NodeType.AUGASSIGN):    
            tNode = self.convertNode(node.target)
            dataDict['target'] = tNode
            opNode = self.convertNode(node.operator)
            dataDict['operator'] = opNode
            vNode = self.convertNode(node.value)
            dataDict['value'] = vNode
            sNode = self.convertNode(node.semicolon) # could be a MaybeSentinel, need to handle
            dataDict['semicolon'] = sNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([tNode, opNode, vNode, sNode])
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
            nNode = self.convertNode(node.name)
            dataDict['name'] = nNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            baseNode = []
            for n in node.bases:
                baseNode.append(self.convertNode(n))
            dataDict['bases'] = baseNode
            kNode = []
            for n in node.keywords:
                kNode.append(self.convertNode(n))
            dataDict['keywords'] = kNode
            dNode = []
            for n in node.decorators:
                dNode.append(self.convertNode(n))
            dataDict['decorators'] = dNode
            lparNode = self.convertNode(node.lpar)
            dataDict['leftParenthesis'] = lparNode
            rparNode = self.convertNode(node.rpar)
            dataDict['rightParenthesis'] = rparNode
            lLNode = []
            for n in node.leading_lines:
                lLNode.append(self.convertNode(n))
            dataDict['leadingLines'] = lLNode
            lADNode = []
            for n in node.lines_after_decorators:
                lADNode.append(self.convertNode(n))
            dataDict['linesAfterDecorators'] = lADNode
            wAClassNode = self.convertNode(node.whitespace_after_class)
            dataDict['whitespaceAfterClass'] = wAClassNode
            wANode = self.convertNode(node.whitespace_after_name)
            dataDict['whitespaceAfterName'] = wANode
            wBColonNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wBColonNode
            if(hasattr(node, 'type_parameters')):
                tPNode = self.convertNode(node.type_parameters)
            else:
                tPNode = None
            dataDict['typeParameters'] = tPNode
            wATPNode = self.convertNode(node.whitespace_after_type_parameters)
            dataDict['whitespaceAfterTypeParameters'] = wATPNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([nNode, bNode, baseNode, dNode, kNode,
                                  lparNode, rparNode, lLNode, lADNode,
                                  wAClassNode, wANode, wBColonNode,
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
                
        return mNode
    
    def unconvertNode(self, mNode):
        if (mNode is None):
            return None
        node = None
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

        dataDict = mNode.dataDict
        if(mNode.nodeType in basicOps):
            wBNode = self.unconvertNode(dataDict['whitespaceBefore'])
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])    
            match mNode.nodeType:
                case NodeType.ADD:
                    node = cst.Add(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.ADDASSIGN:
                    node = cst.AddAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.SUBTRACT:
                    node = cst.Subtract(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.SUBTRACTASSIGN:
                    node = cst.SubtractAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.MULTIPLY:
                    node = cst.Multiply(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.MULTIPLYASSIGN:
                    node = cst.MultiplyAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.DIVIDE:
                    node = cst.Divide(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.DIVIDEASSIGN:
                    node = cst.DivideAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.MODULO:
                    node = cst.Modulo(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.MODULOASSIGN:
                    node = cst.ModuloAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.BITAND:
                    node = cst.BitAnd(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.BITANDASSIGN:
                    node = cst.BitAndAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.BITOR:
                    node = cst.BitOr(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.BITORASSIGN:
                    node = cst.BitOrAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.POWER:
                    node = cst.Power(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.COMMA:
                    node = cst.Comma(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.LESSTHAN:
                    node = cst.LessThan(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.GREATERTHAN:
                    node = cst.GreaterThan(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.EQUAL:
                    node = cst.Equal(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.LESSTHANEQUAL:
                    node = cst.LessThanEqual(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.GREATERTHANEQUAL:
                    node = cst.GreaterThanEqual(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.AND:
                    node = cst.And(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.OR:
                    node = cst.Or(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.IS:
                    node = cst.Is(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.ASSIGNEQUAL:
                    node = cst.AssignEqual(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.SEMICOLON:
                    node = cst.Semicolon(whitespace_before=wBNode, whitespace_after=wANode)
                case _:
                    raise ValueError(f"Unknown node type: {mNode.nodeType}")
        elif(mNode.nodeType == NodeType.NOTEQUAL):
            wBNode = self.unconvertNode(dataDict['whitespaceBefore'])
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])
            node = cst.NotEqual(value=mNode.value, whitespace_before=wBNode, whitespace_after=wANode)
        elif(mNode.nodeType == NodeType.MODULE):
            bNode = []
            for n in dataDict['body']:
                bNodeChild = self.unconvertNode(n)
                bNode.append(bNodeChild)
            hNode = []
            for n in dataDict['header']:
                hNodeChild = self.unconvertNode(n)
                hNode.append(hNodeChild)
            fNode = []
            for n in dataDict['footer']:
                fNodeChild = self.unconvertNode(n)
                fNode.append(fNodeChild)
            node = cst.Module(body=bNode, header=hNode, footer=fNode, encoding=dataDict['encoding'], default_indent=dataDict['defaultIndent'], default_newline=dataDict['defaultNewline'], has_trailing_newline=dataDict['hasTrailingNewline'])
        elif(mNode.nodeType == NodeType.EMPTYLINE):
            wNode = self.unconvertNode(dataDict['whitespace'])
            cNode = self.unconvertNode(dataDict['comment'])
            nNode = self.unconvertNode(dataDict['newline'])
            if cNode:
                node = cst.EmptyLine(indent=dataDict['indent'], whitespace=wNode, comment=cNode, newline=nNode)
            else:
                node = cst.EmptyLine(indent=dataDict['indent'], whitespace=wNode, newline=nNode)
        elif(mNode.nodeType == NodeType.SIMPLEWHITESPACE):
            node = cst.SimpleWhitespace(value=mNode.value)
        elif(mNode.nodeType == NodeType.COMMENT):
            node = cst.Comment(value=mNode.value)
        elif(mNode.nodeType == NodeType.NEWLINE):
            node = cst.Newline(value=mNode.value)
        elif(mNode.nodeType == NodeType.FUNCTIONDEF):
            nNode = self.unconvertNode(dataDict['name'])
            pNode = self.unconvertNode(dataDict['params'])
            bNode = self.unconvertNode(dataDict['body'])
            dNode = []
            for n in dataDict['decorators']:
                dNode.append(self.unconvertNode(n))
            rNode = self.unconvertNode(dataDict['returns'])
            aNode = self.unconvertNode(dataDict['asynchronous'])
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            lADNode = []
            for n in dataDict['linesAfterDecorators']:
                lADNode.append(self.unconvertNode(n))
            wADNode = self.unconvertNode(dataDict['whitespaceAfterDef'])
            wANNode = self.unconvertNode(dataDict['whitespaceAfterName'])
            wBPNode = self.unconvertNode(dataDict['whitespaceBeforeParams'])
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            tPNode = self.unconvertNode(dataDict['typeParameters'])
            wATPNode = self.unconvertNode(dataDict['whitespaceAfterTypeParameters'])
            node = cst.FunctionDef(name=nNode, params=pNode, body=bNode, decorators=dNode, returns=rNode, asynchronous=aNode, leading_lines=lLNode, lines_after_decorators=lADNode, whitespace_after_def=wADNode, whitespace_after_name=wANNode, whitespace_before_params=wBPNode, whitespace_before_colon=wBCNode, type_parameters=tPNode, whitespace_after_type_parameters=wATPNode)
        elif(mNode.nodeType == NodeType.NAME):
            lNode = []
            for n in dataDict['lpar']:
                lNode.append(self.unconvertNode(n))
            rNode = []
            for n in dataDict['rpar']:
                rNode.append(self.unconvertNode(n))
            node = cst.Name(value=mNode.value, lpar=lNode, rpar=rNode)
        elif(mNode.nodeType == NodeType.PARAMETERS):
            pNode = []
            for n in dataDict['params']:
                pNode.append(self.unconvertNode(n))
            sANode = self.unconvertNode(dataDict['starArg'])
            kPNode = []
            for n in dataDict['kwonlyParams']:
                kPNode.append(self.unconvertNode(n))
            sKNode = self.unconvertNode(dataDict['starKwarg'])
            pPNode = []
            for n in dataDict['posonlyParams']:
                pPNode.append(self.unconvertNode(n))
            pINode = self.unconvertNode(dataDict['posonlyInd'])
            node = cst.Parameters(params=pNode, star_arg=sANode, kwonly_params=kPNode, star_kwarg=sKNode, posonly_params=pPNode, posonly_ind=pINode)
        elif(mNode.nodeType == NodeType.INDENTEDBLOCK):
            bNode = []
            for n in dataDict['body']:
                bNode.append(self.unconvertNode(n))
            hNode = self.unconvertNode(dataDict['header'])
            indent = dataDict['indent']
            fNode = []
            for n in dataDict['footer']:
                fNode.append(self.unconvertNode(n))
            node = cst.IndentedBlock(body=bNode, header=hNode, indent=indent, footer=fNode)
        elif(mNode.nodeType == NodeType.TRAILINGWHITESPACE):
            wNode = self.unconvertNode(dataDict['whitespace'])
            cNode = self.unconvertNode(dataDict['comment'])
            nNode = self.unconvertNode(dataDict['newline'])
            node = cst.TrailingWhitespace(whitespace=wNode, comment=cNode, newline=nNode)
        elif(mNode.nodeType == NodeType.SIMPLESTATEMENTLINE):
            bNode = []
            for n in dataDict['body']:
                bNode.append(self.unconvertNode(n))
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            tWNode = self.unconvertNode(dataDict['trailingWhitespace'])
            node = cst.SimpleStatementLine(body=bNode, leading_lines=lLNode, trailing_whitespace=tWNode)
        elif(mNode.nodeType == NodeType.EXPR):
            sNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Expr(value=mNode.value, semicolon=sNode)
        elif(mNode.nodeType == NodeType.CALL):
            fNode = self.unconvertNode(dataDict['func'])
            aNode = []
            for n in dataDict['args']:
                aNode.append(self.unconvertNode(n))
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            wAFNode = self.unconvertNode(dataDict['whitespaceAfterFunc'])
            wBANode = self.unconvertNode(dataDict['whitespaceBeforeArgs'])
            node = cst.Call(func=fNode, args=aNode, lpar=lparNode, rpar=rparNode, whitespace_after_func=wAFNode, whitespace_before_args=wBANode)
        elif(mNode.nodeType == NodeType.ARG):
            valueNode = self.unconvertNode(dataDict['value'])
            keywordNode = self.unconvertNode(dataDict['keyword'])
            equalNode = self.unconvertNode(dataDict['equal'])
            commaNode = self.unconvertNode(dataDict['comma'])
            star = dataDict['star']
            wasNode = self.unconvertNode(dataDict['whitespaceAfterStar'])
            waaNode = self.unconvertNode(dataDict['whitespaceAfterArg'])
            node = cst.Arg(value=valueNode, keyword=keywordNode, equal=equalNode, comma=commaNode, star=star, 
                           whitespace_after_star=wasNode, whitespace_after_arg=waaNode)
        elif(mNode.nodeType == NodeType.SIMPLESTRING):
            value = mNode.value
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.SimpleString(value=value, lpar=lparNode, rpar=rparNode)    
        elif(mNode.nodeType == NodeType.RETURN):
            vNode = self.unconvertNode(dataDict['value'])
            warNode = self.unconvertNode(dataDict['whitespaceAfterReturn']) 
            sNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Return(value=vNode, whitespace_after_return=warNode, semicolon=sNode)
        elif(mNode.nodeType == NodeType.ASSIGN):
            tNode = []
            for n in dataDict['targets']:
                tNode.append(self.unconvertNode(n))
            vNode = self.unconvertNode(dataDict['value'])
            sNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Assign(targets=tNode, value=vNode, semicolon=sNode)
        elif(mNode.nodeType == NodeType.ASSIGNTARGET):                        
            tNode = self.unconvertNode(dataDict['target'])
            wbeNode = self.unconvertNode(dataDict['whitespaceBeforeEqual'])
            waeNode = self.unconvertNode(dataDict['whitespaceAfterEqual'])
            node = cst.AssignTarget(target=tNode, whitespace_before_equal=wbeNode, whitespace_after_equal=waeNode)
        elif(mNode.nodeType == NodeType.LIST):
            eNode = []
            for n in dataDict['elements']:
                eNode.append(self.unconvertNode(n)) 
            lbNode = self.unconvertNode(dataDict['leftBracket'])    
            rbNode = self.unconvertNode(dataDict['rightBracket'])
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.List(elements=eNode, lbracket=lbNode, rbracket=rbNode, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType == NodeType.LEFTSQUAREBRACKET or mNode.nodeType == NodeType.LEFTPAREN):            
            waNode = self.unconvertNode(dataDict['whitespaceAfter'])
            match mNode.nodeType:
                case NodeType.LEFTSQUAREBRACKET:   
                    node = cst.LeftSquareBracket(whitespace_after=waNode)
                case NodeType.LEFTPAREN:
                    node = cst.LeftParen(whitespace_after=waNode)
        elif(mNode.nodeType == NodeType.RIGHTSQUAREBRACKET or mNode.nodeType == NodeType.RIGHTPAREN):
            wbNode = self.unconvertNode(dataDict['whitespaceBefore'])
            match mNode.nodeType:
                case NodeType.RIGHTSQUAREBRACKET:
                    node = cst.RightSquareBracket(whitespace_before=wbNode)
                case NodeType.RIGHTPAREN:
                    node = cst.RightParen(whitespace_before=wbNode)
        elif(mNode.nodeType == NodeType.ELEMENT):
            vNode = self.unconvertNode(dataDict['value'])
            cNode = self.unconvertNode(dataDict['comma'])
            node = cst.Element(value=vNode, comma=cNode)
        elif(mNode.nodeType == NodeType.INTEGER):
            value = mNode.value
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:  
                rparNode.append(self.unconvertNode(n))
            node = cst.Integer(value=value, lpar=lparNode, rpar=rparNode)                
        elif(mNode.nodeType == NodeType.BINARYOPERATION):
            lNode = self.unconvertNode(dataDict['left'])
            opNode = self.unconvertNode(dataDict['operator'])
            rNode = self.unconvertNode(dataDict['right'])
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.BinaryOperation(left=lNode, operator=opNode, right=rNode, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType == NodeType.FOR):
            targetNode = self.unconvertNode(dataDict['target'])
            iterNode = self.unconvertNode(dataDict['iter'])
            bNode = self.unconvertNode(dataDict['body'])
            orElseNode = self.unconvertNode(dataDict['orelse'])
            asyncNode = self.unconvertNode(dataDict['asynchronous'])
            leadLineNode = []
            for n in dataDict['leadingLines']: 
                leadLineNode.append(self.unconvertNode(n))
            wsafNode = self.unconvertNode(dataDict['whitespaceAfterFor'])
            wsbiNode = self.unconvertNode(dataDict['whitespaceBeforeIn'])
            wsaiNode = self.unconvertNode(dataDict['whitespaceAfterIn'])
            wsbcNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.For(target=targetNode, iter=iterNode, body=bNode, orelse=orElseNode, 
                           asynchronous=asyncNode, leading_lines=leadLineNode, whitespace_after_for=wsafNode, 
                           whitespace_before_in=wsbiNode, whitespace_after_in=wsaiNode, whitespace_before_colon=wsbcNode)
        elif(mNode.nodeType == NodeType.AUGASSIGN):    
            tNode = self.unconvertNode(dataDict['target'])
            opNode = self.unconvertNode(dataDict['operator'])   
            vNode = self.unconvertNode(dataDict['value'])
            sNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.AugAssign(target=tNode, operator=opNode, value=vNode, semicolon=sNode)
        elif(mNode.nodeType == NodeType.UNARYOPERATION):
            opNode = self.unconvertNode(dataDict['operator'])
            exNode = self.unconvertNode(dataDict['expression'])
            lparNode = []
            for n in dataDict['lpar']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rpar']:
                rparNode.append(self.unconvertNode(n))  
            node = cst.UnaryOperation(operator=opNode, expression=exNode, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType in unaryOps):
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])  
            match mNode.nodeType:
                case NodeType.BITINVERT:
                    node = cst.BitInvert(whitespace_after=wANode)
                case NodeType.MINUS:
                    node = cst.Minus(whitespace_after=wANode)
                case NodeType.NOT:
                    node = cst.Not(whitespace_after=wANode)
                case NodeType.PLUS:
                    node = cst.Plus(whitespace_after=wANode)
                case _:
                    raise ValueError(f"Unknown node type: {mNode.nodeType}")            
        elif(mNode.nodeType == NodeType.COMPARISON):
            lNode = self.unconvertNode(dataDict['left'])
            compsNode = []
            for n in dataDict['comparisons']:
                compsNode.append(self.unconvertNode(n))
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.Comparison(left=lNode, comparisons=compsNode, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType == NodeType.COMPARISONTARGET):
            opNode = self.unconvertNode(dataDict['operator'])
            compNode = self.unconvertNode(dataDict['comparator'])
            node = cst.ComparisonTarget(operator=opNode, comparator=compNode)
        elif(mNode.nodeType == NodeType.BOOLEANOPERATION):
            lNode = self.unconvertNode(dataDict['left'])
            opNode = self.unconvertNode(dataDict['operator'])
            rNode = self.unconvertNode(dataDict['right'])
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.BooleanOperation(left=lNode, operator=opNode, right=rNode, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType == NodeType.IFEXP):
            testNode = self.unconvertNode(dataDict['test'])
            bodyNode = self.unconvertNode(dataDict['body'])
            orelseNode = self.unconvertNode(dataDict['orelse'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            wBINode = self.unconvertNode(dataDict['whitespaceBeforeIf'])
            wAINode = self.unconvertNode(dataDict['whitespaceAfterIf'])
            wBENode = self.unconvertNode(dataDict['whitespaceBeforeElse'])
            wAENode = self.unconvertNode(dataDict['whitespaceAfterElse'])
            node = cst.IfExp(test=testNode, body=bodyNode, orelse=orelseNode, lpar=lParNode, rpar=rParNode,
                    whitespace_before_if=wBINode, whitespace_after_if=wAINode, whitespace_before_else=wBENode, whitespace_after_else=wAENode)
        elif(mNode.nodeType == NodeType.CLASSDEF):    
            nNode = self.unconvertNode(dataDict['name'])
            bNode = self.unconvertNode(dataDict['body'])
            baseNode = []   
            for n in dataDict['bases']:
                baseNode.append(self.unconvertNode(n))
            dNode = []
            for n in dataDict['decorators']:
                dNode.append(self.unconvertNode(n))
            kNode = []
            for n in dataDict['keywords']:
                kNode.append(self.unconvertNode(n))
            lparNode = self.unconvertNode(dataDict['leftParenthesis'])
            rparNode = self.unconvertNode(dataDict['rightParenthesis'])
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            lADNode = []
            for n in dataDict['linesAfterDecorators']:
                lADNode.append(self.unconvertNode(n))
            wAClassNode = self.unconvertNode(dataDict['whitespaceAfterClass'])
            wANode = self.unconvertNode(dataDict['whitespaceAfterName'])
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            tPNode = self.unconvertNode(dataDict['typeParameters'])
            wATPNode = self.unconvertNode(dataDict['whitespaceAfterTypeParameters'])
            node = cst.ClassDef(name=nNode, body=bNode, bases=baseNode, decorators=dNode, keywords=kNode, 
                    lpar=lparNode, rpar=rparNode, leading_lines=lLNode, lines_after_decorators=lADNode, 
                    whitespace_after_class=wAClassNode, whitespace_after_name=wANode, whitespace_before_colon=wBCNode,
                    type_parameters=tPNode, whitespace_after_type_parameters=wATPNode)
        elif(mNode.nodeType == NodeType.PARAM):
            nNode = self.unconvertNode(dataDict['name'])
            aNode = self.unconvertNode(dataDict['annotation'])
            eNode = self.unconvertNode(dataDict['equal'])
            dNode = self.unconvertNode(dataDict['default'])
            cNode = self.unconvertNode(dataDict['comma'])
            sNode = self.unconvertNode(dataDict['star'])
            wASNode = self.unconvertNode(dataDict['whitespaceAfterStar'])
            wAPNode = self.unconvertNode(dataDict['whitespaceAfterParam'])
            node = cst.Param(name=nNode, annotation=aNode, equal=eNode, default=dNode, 
                             comma=cNode, star=sNode, whitespace_after_star=wASNode, 
                             whitespace_after_param=wAPNode)
        elif(mNode.nodeType == NodeType.PARAMSTAR):
            cNode = self.unconvertNode(dataDict['comma'])
            node = cst.ParamStar(comma=cNode)
        elif(mNode.nodeType == NodeType.ANNOTATION):
            aNode = self.unconvertNode(dataDict['annotation'])
            wBINode = self.unconvertNode(dataDict['whitespaceBeforeIndicator'])
            wAINode = self.unconvertNode(dataDict['whitespaceAfterIndicator'])
            node = cst.Annotation(annotation=aNode, whitespace_before_indicator=wBINode, whitespace_after_indicator=wAINode)
        elif(mNode.nodeType == NodeType.MAYBESENTINEL):
            node = cst.MaybeSentinel.DEFAULT

        return node
    
    def getRowNumber(self, node):
        # wrapper = cst.metadata.MetadataWrapper(node)
        # positions = wrapper.resolve(PositionProvider)
        # print("Row number is: " + positions.line)
        # return positions.line
        try:
            pos = self.metadata[node]
            print("Row number is: " + str(pos.start.line))
            return pos.start.line
        except Exception:
            print("Error in getting row number")
            return -1
    
    def getColNumber(self, node):
        # wrapper = cst.metadata.MetadataWrapper(node)
        # positions = wrapper.resolve(PositionProvider)
        # print("Row number is: " + positions.column)
        # return positions.column
        try:
            pos = self.metadata[node]
            print("Column number is: " + str(pos.start.column))
            return pos.start.column
        except Exception:
            print("Error in getting column number")
            return -1
        return 0
    
# class VisitNodes(cst.CSTVisitor):
#     METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)
#     global lst

#     def on_visit(self, node):
#         # Called every time a node is visited, before we've visited its children.

#         # Returns ``True`` if children should be visited, and returns ``False``
#         # otherwise

#         with open("test.txt", "a", encoding='utf-8') as f:
#             if type(node).__name__ not in lst:
#                 print(lst)
#                 lst.append(type(node).__name__)
#                 f.write(type(node).__name__ + '\n')
#             # f.write(type(node).__name__ + '\n')
#             # print(type(node).__name__)
#         visit_func = getattr(self, f"visit_{type(node).__name__}", None)
#         if visit_func is not None:
#             retval = visit_func(node)
#         else:
#             retval = True
#         # Don't visit children IFF the visit function returned False.
#         return False if retval is False else True
    