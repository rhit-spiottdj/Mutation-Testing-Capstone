from Mutator.MutationTree import MutationTree
from Mutator.MutationTree import MutationNode
from Mutator.NodeTypes import NodeType
import os
# import tree_sitter_python as tspython
# from tree_sitter import Language, Parser
import libcst as cst
from libcst.metadata import PositionProvider

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
        "Annotation" : NodeType.ANNOTATION,
        "Semicolon" : NodeType.SEMICOLON,
        "If" : NodeType.IF,
        "Else" : NodeType.ELSE, 
        # 'New' Nodes. 'Done' Means the convert is done but not the unconvert
        "Attribute" : NodeType.ATTRIBUTE, #Done
        "Asynchronous" : NodeType.ASYNCHRONOUS, #Done
        "Await" : NodeType.AWAIT, #Done
        "Yield" : NodeType.YIELD, #Done
        "From" : NodeType.FROM, #Done
        "Lambda" : NodeType.LAMBDA, #Done
        "Ellipsis" : NodeType.ELLIPSIS, #Done
        "Float" : NodeType.FLOAT, #Done
        "Imaginary" : NodeType.IMAGINARY, #Done
        "ConcatenatedString" : NodeType.CONCATENATEDSTRING, #Done
        "FormattedString" : NodeType.FORMATTEDSTRING, #Done
        "FormattedStringText" : NodeType.FORMATTEDSTRINGTEXT, #Done
        "FormattedStringExpression" : NodeType.FORMATTEDSTRINGEXPRESSION, #Done
        "Tuple" : NodeType.TUPLE, #Done
        "Set" : NodeType.SET, #Done
        "StarredElement" : NodeType.STARREDELEMENT, #Done
        "Dict" : NodeType.DICT,
        "DictElement" : NodeType.DICTELEMENT,
        "StarredDictElement" : NodeType.STARREDDICTELEMENT,
        "GeneratorExp" : NodeType.GENERATOREXP,
        "ListComp" : NodeType.LISTCOMP,
        "SetComp" : NodeType.SETCOMP,
        "DictComp" : NodeType.DICTCOMP,
        "CompFor" : NodeType.COMPFOR,
        "CompIf" : NodeType.COMPIF,
        "Subscript" : NodeType.SUBSCRIPT,
        "Index" : NodeType.INDEX,
        "Slice" : NodeType.SLICE,
        "SubscriptElement" : NodeType.SUBSCRIPTELEMENT,
        "LeftCurlyBrace" : NodeType.LEFTCURLYBRACE, #Done
        "RightCurlyBrace" : NodeType.RIGHTCURLYBRACE, #Done
        "AnnAssign" : NodeType.ANNASSIGN,
        "Assert" : NodeType.ASSERT,
        "Break" : NodeType.BREAK,
        "Continue" : NodeType.CONTINUE,
        "Del" : NodeType.DEL,
        "Global" : NodeType.GLOBAL,
        "Import" : NodeType.IMPORT,
        "ImportFrom" : NodeType.IMPORTFROM,
        "NonLocal" : NodeType.NONLOCAL,
        "Pass" : NodeType.PASS,
        "Raise" : NodeType.RAISE,
        "Try" : NodeType.TRY,
        "While" : NodeType.WHILE,
        "With" : NodeType.WITH,
        "AsName" : NodeType.ASNAME,
        "Decorator" : NodeType.DECORATOR,
        "ExceptHandler" : NodeType.EXCEPTHANDLER,
        "Finally" : NodeType.FINALLY,
        "ImportAlias" : NodeType.IMPORTALIAS,
        "NameItem" : NodeType.NAMEITEM,
        "ParamSlash" : NodeType.PARAMSLASH,
        "WithItem" : NodeType.WITHITEM,
        "SimpleStatementSuite" : NodeType.SIMPLESTATEMENTSUITE,
        "BitXor" : NodeType.BITXOR, #Done
        "FloorDivide" : NodeType.FLOORDIVIDE, #Done
        "LeftShift" : NodeType.LEFTSHIFT, #Done
        "MatrixMultiply" : NodeType.MATRIXMULTIPLY, #Done
        "RightShift" : NodeType.RIGHTSHIFT, #Done
        "In" : NodeType.IN, #Done
        "IsNot" : NodeType.ISNOT, #Done
        "NotIn" : NodeType.NOTIN, #Done
        "BitXorAssign" : NodeType.BITXORASSIGN, #Done
        "FloorDivideAssign" : NodeType.FLOORDIVIDEASSIGN, #Done
        "LeftShiftAssign" : NodeType.LEFTSHIFTASSIGN, #Done
        "MatrixMultiplyAssign" : NodeType.MATRIXMULTIPLYASSIGN, #Done
        "PowerAssign" : NodeType.POWERASSIGN, #Done
        "RightShiftAssign" : NodeType.RIGHTSHIFTASSIGN, #Done
        "Colon" : NodeType.COLON,
        "Dot" : NodeType.DOT,
        "ImportStar" : NodeType.IMPORTSTAR,
        "ParenthesizedWhitespace" : NodeType.PARENTHESIZEDWHITESPACE,
        # Base Nodes, used for "is instance" not needed to be converted I think
        "BaseUnaryOp" : NodeType.BASEUNARYOP,
        "BaseBooleanOp" : NodeType.BASEBOOLEANOP,
        "BaseCompOp" : NodeType.BASECOMPOP,
        "BaseBinaryOp" : NodeType.BASEBINARYOP,
        "BaseAssignTargetExpression" : NodeType.BASEASSIGNTARGETEXPRESSION,
        "BaseDelTargetExpression" : NodeType.BASEDELTARGETEXPRESSION,
        "BaseComp" : NodeType.BASECOMP,
        "BaseSimpleComp" : NodeType.BASESIMPLECOMP,
        "BaseSuite" : NodeType.BASESUITE,
        "BaseSmallStatement" : NodeType.BASESMALLSTATEMENT,
        "BaseSlice" : NodeType.BASESLICE,
        "BaseDictElement" : NodeType.BASEDICTELEMENT,
        "BaseCompoundStatement" : NodeType.BASECOMPOUNDSTATEMENT,
        "BaseParenthesizableWhitespace" : NodeType.BASEPARENTHESIZABLEWHITESPACE,
        "BaseExpression" : NodeType.BASEEXPRESSION,
        "BaseNumber" : NodeType.BASENUMBER,
        "BaseString" : NodeType.BASESTRING,
        "BaseFormattedStringContent" : NodeType.BASEFORMATTEDSTRINGCONTENT,
        "BaseList" : NodeType.BASELIST,
        "BaseSet" : NodeType.BASESET,
        "BaseElement" : NodeType.BASEELEMENT,
        "BaseDict" : NodeType.BASEDICT,
    }

    # parser = Parser(PY_LANGUAGE)
    # treeSitter = None
    original_code = None
    file = ""
    C = ""
    
    def __init__(self, file_path, C):
        self.file = file_path
        self.C = C
        abs_path = os.path.normpath(os.path.join(C, file_path))
        # Compute full path to the file using os.path.join to avoid missing separators
        file_fullpath = os.path.normpath(os.path.join(self.C, self.file))
        with open(file_fullpath, 'r', encoding='utf-8') as fd:
            self.original_code = fd.read()
        fd.close()

        print('OG file dest: ' + abs_path + '\n') #debug
        

    def getTree(self):
        wrapper = cst.MetadataWrapper(cst.parse_module(self.original_code))
        self.metadata = wrapper.resolve(PositionProvider)
        module_with_metadata = wrapper.module
        mTree = self.makeMTree(module_with_metadata) # Convert to our tree
        return mTree

    def makeMTree(self, tree):
        mTree = MutationTree(self.convertNode(tree))
        return mTree
    
    def unmakeMTree(self, mTree):
        # do conversion back to library tree
        headNode = self.unconvertNode(mTree.headNode)
        return headNode

    def loadOriginalCode(self):
        # load originalCode
        file_fullpath = os.path.normpath(os.path.join(self.C, self.file))
        with open(file_fullpath, 'w', encoding='utf-8') as fd:
            fd.write(self.original_code)
            fd.flush()
            fd.close()
        return

    def loadMutatedCode(self, mTree):
        mutatedCode = self.backToCode(mTree)

        #load mutation
        file_fullpath = os.path.normpath(os.path.join(self.C, self.file))
        with open(file_fullpath, 'w', encoding='utf-8') as fd:
            fd.write(mutatedCode)
            fd.flush()
            fd.close()
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
                    NodeType.BITXOR, NodeType.BITXORASSIGN,
                    NodeType.FLOORDIVIDE, NodeType.FLOORDIVIDEASSIGN,
                    NodeType.LEFTSHIFT, NodeType.LEFTSHIFTASSIGN,
                    NodeType.RIGHTSHIFT, NodeType.RIGHTSHIFTASSIGN,
                    NodeType.MATRIXMULTIPLY, NodeType.MATRIXMULTIPLYASSIGN,
                    NodeType.POWER, NodeType.POWERASSIGN, NodeType.COMMA,
                    NodeType.LESSTHAN, NodeType.GREATERTHAN, NodeType.EQUAL,
                    NodeType.LESSTHANEQUAL, NodeType.GREATERTHANEQUAL,
                    NodeType.AND, NodeType.OR, NodeType.IS, NodeType.IN, NodeType.ASSIGNEQUAL, 
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
                bNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
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
        elif(newType == NodeType.SIMPLEWHITESPACE or newType == NodeType.FORMATTEDSTRINGTEXT):
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
        elif(newType == NodeType.SIMPLESTRING or newType == NodeType.ELLIPSIS):
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
        elif(newType == NodeType.LEFTSQUAREBRACKET or newType == NodeType.LEFTPAREN or newType == NodeType.LEFTCURLYBRACE):
            waNode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = waNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([waNode])
        elif(newType == NodeType.RIGHTSQUAREBRACKET or newType == NodeType.RIGHTPAREN or newType == NodeType.RIGHTCURLYBRACE):
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
        elif(newType == NodeType.INTEGER or newType == NodeType.FLOAT or newType == NodeType.IMAGINARY):
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
            nNode = self.convertNode(node.name)
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
            mNode.attachChildren([nNode, aNode, eNode, dNode, cNode, sNode, wASNode, wAPNode])
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
        elif(newType == NodeType.IF):
            tNode = self.convertNode(node.test)
            dataDict['test'] = tNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            if(hasattr(node, 'orelse')):
                oENode = self.convertNode(node.orelse)
            else:
                oENode = None
            dataDict['orelse'] = oENode
            lLNode = []
            for n in node.leading_lines:
                lLNode.append(self.convertNode(n))
            dataDict['leadingLines'] = lLNode
            wBTNode = self.convertNode(node.whitespace_before_test)
            dataDict['whitespaceBeforeTest'] = wBTNode
            wATNode = self.convertNode(node.whitespace_after_test)
            dataDict['whitespaceAfterTest'] = wATNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
        elif(newType == NodeType.ELSE):
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            lLNode = []
            for n in node.leading_lines:
                lLNode.append(self.convertNode(n))
            dataDict['leadingLines'] = lLNode
            wBCNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wBCNode
        elif(newType == NodeType.ATTRIBUTE):
            valueNode = self.convertNode(node.value)
            dataDict['value'] = valueNode
            atNode = self.convertNode(node.attr)
            dataDict['attr'] = atNode
            dNode = self.convertNode(node.dot)
            dataDict['dot'] = dNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([valueNode, atNode, dNode, lparNode, rparNode])
        elif(newType == NodeType.ASYNCHRONOUS):
            wANode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = wANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachOneChild(wANode)
        elif(newType == NodeType.AWAIT):
            eNode = self.convertNode(node.expression)
            dataDict['expression'] = eNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            wAANode = self.convertNode(node.whitespace_after_await)
            dataDict['whitespaceAfterAwait'] = wAANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([eNode, lparNode, rparNode, wAANode])
        elif(newType == NodeType.YIELD):
            if(hasattr(node, 'value')):
                valueNode = self.convertNode(node.value)
            else:
                valueNode = None
            dataDict['value'] = valueNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            wAYNode = self.convertNode(node.whitespace_after_yield)
            dataDict['whitespaceAfterAwait'] = wAYNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([valueNode, lparNode, rparNode, wAYNode])
        elif(newType == NodeType.FROM):
            iNode = self.convertNode(node.item)
            dataDict['item'] = iNode
            wBFNode = self.convertNode(node.whitespace_before_from)
            dataDict['whitespaceBeforeFrom'] = wBFNode
            wAFNode = self.convertNode(node.whitespace_after_from)
            dataDict['whitespaceAfterFrom'] = wAFNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([iNode, wBFNode, wAFNode])
        elif(newType == NodeType.LAMBDA):
            pNode = self.convertNode(node.params)
            dataDict['params'] = pNode
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            cNode = self.convertNode(node.colon)
            dataDict['colon'] = cNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            wALNode = self.convertNode(node.whitespace_after_lambda)
            dataDict['whitespaceAfterLambda'] = wALNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([pNode, bNode, cNode, lparNode, rparNode, wALNode])
        elif(newType == NodeType.PARAMSLASH):
            cNode = self.convertNode(node.comma)
            dataDict['comma'] = cNode
            wAYNode = self.convertNode(node.whitespace_after_yield)
            dataDict['whitespaceAfterAwait'] = wAYNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([cNode, wAYNode])
        elif(newType == NodeType.CONCATENATEDSTRING):
            lNode = self.convertNode(node.left)
            dataDict['left'] = lNode
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
            wBNode = self.convertNode(node.whitespace_between)
            dataDict['whitespaceBetween'] = wBNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([lNode, rNode, lparNode, rparNode, wBNode])
        elif(newType == NodeType.FORMATTEDSTRING):
            pNode = []
            for n in node.parts:
                pNode.append(self.convertNode(n))
            dataDict['parts'] = pNode
            dataDict['start'] = node.start
            dataDict['end'] = node.end
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([pNode, lparNode, rparNode])
        elif(newType == NodeType.FORMATTEDSTRINGEXPRESSION):
            eNode = self.convertNode(node.expression)
            dataDict['expression'] = eNode
            if(hasattr(node, 'conversion')):
                dataDict['conversion'] = node.conversion
            else:
                dataDict['conversion'] = None
            if(hasattr(node, 'format_spec')):
                fSNode = []
                for n in node.format_spec:
                    fSNode.append(self.convertNode(n))
            else:
                fSNode = None
            dataDict['format_spec'] = fSNode    
            wBENode = self.convertNode(node.whitespace_before_expresion)
            dataDict['whitespaceBeforeExpression'] = wBENode
            wAENode = self.convertNode(node.whitespace_after_expression)
            dataDict['whitespaceAfterExpression'] = wAENode
            if(hasattr(node, 'equal')):
                eqNode = self.convertNode(node.equal)
            else:
                eqNode = None
            dataDict['equal'] = eqNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([eNode, fSNode, wBENode, wAENode, eqNode])
        elif(newType == NodeType.NOTIN or newType == NodeType.ISNOT):
            wBNode = self.convertNode(node.whitespace_before)
            dataDict['whitespaceBefore'] = wBNode
            wBTNode = self.convertNode(node.whitespace_between)
            dataDict['whitespaceBetween'] = wBTNode
            wANode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = wANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wBNode, wBTNode, wANode])
        elif(newType == NodeType.TUPLE or newType == NodeType.SET):
            eNodes = []
            for n in node.elements:
                eNodes.append(self.convertNode(n))
            dataDict['elements'] = eNodes
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            if(newType == NodeType.SET):
                lbraNode = []
                for n in node.lbrace:
                    lbraNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
                dataDict['leftCurlyBrace'] = lbraNode 
                rbraNode = []
                for n in node.rpar:
                    rbraNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
                dataDict['rightCurlyBrace'] = rbraNode
                mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
                mNode.attachChildren([eNodes, lbraNode, rbraNode, lparNode, rparNode])
            else:
                mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
                mNode.attachChildren([eNodes, lparNode, rparNode])
        elif(newType == NodeType.STARREDELEMENT):
            valueNode = self.convertNode(node.value)
            dataDict['value'] = valueNode
            cNode = self.convertNode(node.comma)
            dataDict['comma'] = cNode
            lparNode = []
            for n in node.lpar:
                lparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['leftParenthesis'] = lparNode 
            rparNode = []
            for n in node.rpar:
                rparNode.append(self.convertNode(n)) # do a loop of the contents as it is a sequence of LibCST stuff
            dataDict['rightParenthesis'] = rparNode
            wBVNode = self.convertNode(node.whitespace_before_value)
            dataDict['whitespaceBeforeValue'] = wBVNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)           
            mNode.attachChildren([valueNode, cNode, lparNode, rparNode, wBVNode])
        elif(newType == NodeType.IMPORT):
            nNodes = []
            for n in node.names:
                nNodes.append(self.convertNode(n))
            dataDict['names'] = nNodes
            sNode = self.convertNode(node.semicolon)
            dataDict['semicolon'] = sNode
            wAINode = self.convertNode(node.whitespace_after_import)
            dataDict['whitespaceAfterImport'] = wAINode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([nNodes, sNode, wAINode])
        elif(newType == NodeType.IMPORTFROM):
            moduleNode = self.convertNode(node.module)
            dataDict['module'] = moduleNode
            nNodes = []
            for n in node.names:
                nNodes.append(self.convertNode(n))
            dataDict['names'] = nNodes
            rNode = []
            for n in node.relative:
                rNode.append(self.convertNode(n))
            dataDict['relative'] = rNode
            lparNode = self.convertNode(node.lpar)
            dataDict['leftParenthesis'] = lparNode
            rparNode = self.convertNode(node.rpar)
            dataDict['rightParenthesis'] = rparNode
            sNode = self.convertNode(node.semicolon)
            dataDict['semicolon'] = sNode
            wAFNode = self.convertNode(node.whitespace_after_from)
            dataDict['whitespaceAfterFrom'] = wAFNode
            wBINode = self.convertNode(node.whitespace_before_import)
            dataDict['whitespaceBeforeImport'] = wBINode
            wAINode = self.convertNode(node.whitespace_after_import)
            dataDict['whitespaceAfterImport'] = wAINode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([moduleNode, nNodes, rNode, lparNode, rparNode,
                                  sNode, wAFNode, wBINode, wAINode])
        elif(newType == NodeType.IMPORTALIAS):
            nNode = self.convertNode(node.name)
            dataDict['name'] = nNode
            if(hasattr(node, 'asname')):
              aNode = self.convertNode(node.asname)
            else:
              aNode = None
            dataDict['asname'] = aNode
            cNode = self.convertNode(node.comma)
            dataDict['comma'] = cNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([nNode, aNode, cNode])
        elif(newType == NodeType.DOT):
            wBNode = self.convertNode(node.whitespace_before)
            dataDict['whitespaceBefore'] = wBNode
            wANode = self.convertNode(node.whitespace_after)
            dataDict['whitespaceAfter'] = wANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([wBNode, wANode])
        elif(newType == NodeType.ASNAME):
            name = node.name
            wBANode = self.convertNode(node.whitespace_before_as)
            dataDict['whitespaceBeforeAs'] = wBANode
            wAANode = self.convertNode(node.whitespace_after_as)
            dataDict['whitespaceAfterAs'] = wAANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict, value=name)
            mNode.attachChildren([wBANode, wAANode])
        elif(newType == NodeType.TRY):
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            hNodes = []
            for n in node.handlers:
                hNodes.append(self.convertNode(n))
            dataDict['handlers'] = hNodes
            if(hasattr(node, 'orelse')):
                oENode = self.convertNode(node.orelse)
            else:
                oENode = None
            dataDict['orelse'] = oENode
            if(hasattr(node, 'finalbody')):
                fNode = self.convertNode(node.finalbody)
            else:
                fNode = None
            dataDict['finalbody'] = fNode
            lLNode = []
            for n in node.leading_lines:
                lLNode.append(self.convertNode(n))
            dataDict['leadingLines'] = lLNode
            wBCNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wBCNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, hNodes, oENode, fNode, lLNode, wBCNode])
        elif(newType == NodeType.EXCEPTHANDLER):
            bNode = self.convertNode(node.body)
            dataDict['body'] = bNode
            if(hasattr(node, 'type')):
                tNode = self.convertNode(node.type)
            else:
                tNode = None
            dataDict['type'] = tNode
            if(hasattr(node, 'name')):
                nNode = self.convertNode(node.name)
            else:
                nNode = None
            dataDict['name'] = nNode
            lLNode = []
            for n in node.leading_lines:
                lLNode.append(self.convertNode(n))
            dataDict['leadingLines'] = lLNode
            wAENode = self.convertNode(node.whitespace_after_except)
            dataDict['whitespaceAfterExcept'] = wAENode
            wBCNode = self.convertNode(node.whitespace_before_colon)
            dataDict['whitespaceBeforeColon'] = wBCNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([bNode, tNode, nNode, lLNode, wAENode, wBCNode])
        else:
            raise ValueError(f"Unknown node type: {newType}")

        mNode.setOldType(type(node).__name__)
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
            if (mNode.value is None):
                node = cst.NotEqual(value="!=", whitespace_before=wBNode, whitespace_after=wANode)
            else:
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
            if isinstance(dataDict['star'], str):
                sNode = dataDict['star']
            else:
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
        elif(mNode.nodeType == NodeType.IF):
            tNode = self.unconvertNode(dataDict['test'])
            bNode = self.unconvertNode(dataDict['body'])
            oENode = self.unconvertNode(dataDict['orelse'])
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wBTNode = self.unconvertNode(dataDict['whitespaceBeforeTest'])
            wATNode = self.unconvertNode(dataDict['whitespaceBeforeTest'])
            node = cst.If(test=tNode, body=bNode, orelse=oENode, leading_lines=lLNode, whitespace_before_test=wBTNode, whitespace_after_test=wATNode)
        elif(mNode.nodeType == NodeType.ELSE):
            bNode = self.unconvertNode(dataDict['body'])
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.Else(body=bNode, leading_lines=lLNode, whitespace_before_colon=wBCNode)
        elif(mNode.nodeType == NodeType.TRUE or mNode.nodeType == NodeType.FALSE):
            lPNode = []
            lPNode.append(cst.LeftParen())
            rPNode = []
            rPNode.append(cst.RightParen())
            node = cst.Name(value=mNode.value, lpar=lPNode, rpar=rPNode)
        # elif(mNode.nodeType == NodeType.PARAMSLASH):
        #     cNode = self.unconvertNode(dataDict['comma'])
        #     wASNode = self.unconvertNode(dataDict['whitespaceAfterSlash'])
        #     node = cst.ParamSlash(comma=cNode, whitespace_after_slash=wASNode)

        return node
    
    def getRowNumber(self, node):
        try:
            pos = self.metadata[node]
            # print("Row number is: " + str(pos.start.line))
            return pos.start.line
        except Exception:
            # print("Error in getting row number")
            return -1
    
    def getColNumber(self, node):
        try:
            pos = self.metadata[node]
            # print("Column number is: " + str(pos.start.column))
            return pos.start.column
        except Exception:
            # print("Error in getting column number")
            return -1
    