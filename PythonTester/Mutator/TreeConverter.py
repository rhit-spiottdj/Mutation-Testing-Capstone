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
        "Attribute" : NodeType.ATTRIBUTE, #Done and unconvert done
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
        "Colon" : NodeType.COLON, #TODO CONVERT
        "Dot" : NodeType.DOT,
        "ImportStar" : NodeType.IMPORTSTAR, #TODO CONVERT? Unsure if needed look at libcst docs
        "ParenthesizedWhitespace" : NodeType.PARENTHESIZEDWHITESPACE, #TODO CONVERT
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
            vNode = self.convertNode(node.value)
            dataDict['value'] = vNode
            sNode = self.convertNode(node.semicolon)
            dataDict['semicolon'] = sNode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
            mNode.attachChildren([vNode, sNode])
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
            name = self.convertNode(node.name)
            dataDict['name'] = name
            wBANode = self.convertNode(node.whitespace_before_as)
            dataDict['whitespaceBeforeAs'] = wBANode
            wAANode = self.convertNode(node.whitespace_after_as)
            dataDict['whitespaceAfterAs'] = wAANode
            mNode = MutationNode(newType, rowNumber, colNumber, dataDict)
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
                    NodeType.BITXOR, NodeType.BITXORASSIGN,
                    NodeType.FLOORDIVIDE, NodeType.FLOORDIVIDEASSIGN,
                    NodeType.LEFTSHIFT, NodeType.LEFTSHIFTASSIGN,
                    NodeType.POWER, NodeType.POWERASSIGN,
                    NodeType.RIGHTSHIFT, NodeType.RIGHTSHIFTASSIGN,
                    NodeType.MATRIXMULTIPLY, NodeType.MATRIXMULTIPLYASSIGN,
                    NodeType.COMMA, NodeType.COLON,
                    NodeType.LESSTHAN, NodeType.GREATERTHAN, NodeType.EQUAL,
                    NodeType.LESSTHANEQUAL, NodeType.GREATERTHANEQUAL,
                    NodeType.AND, NodeType.OR, NodeType.IS, NodeType.ASSIGNEQUAL, 
                    NodeType.SEMICOLON, NodeType.ISNOT, NodeType.IN, NodeType.NOTIN]
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
                case NodeType.POWERASSIGN:
                    node = cst.PowerAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.BITXOR:
                    node = cst.BitXor(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.BITXORASSIGN:
                    node = cst.BitXorAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.FLOORDIVIDE:
                    node = cst.FloorDivide(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.FLOORDIVIDEASSIGN:
                    node = cst.FloorDivideAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.LEFTSHIFT:
                    node = cst.LeftShift(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.LEFTSHIFTASSIGN:
                    node = cst.LeftShiftAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.RIGHTSHIFT:
                    node = cst.RightShift(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.RIGHTSHIFTASSIGN:
                    node = cst.RightShiftAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.MATRIXMULTIPLY:
                    node = cst.MatrixMultiply(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.MATRIXMULTIPLYASSIGN:
                    node = cst.MatrixMultiplyAssign(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.IN:
                    node = cst.In(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.NOTIN:
                    node = cst.NotIn(whitespace_before=wBNode, whitespace_after=wANode)
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
                case NodeType.ISNOT:
                    node = cst.IsNot(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.ASSIGNEQUAL:
                    node = cst.AssignEqual(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.SEMICOLON:
                    node = cst.Semicolon(whitespace_before=wBNode, whitespace_after=wANode)
                case NodeType.COLON:
                    node = cst.Colon(whitespace_before=wBNode, whitespace_after=wANode)
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
            vNode = self.unconvertNode(dataDict['value'])
            sNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Expr(value=vNode, semicolon=sNode)
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
        elif(mNode.nodeType == NodeType.ATTRIBUTE):
            vNode = self.unconvertNode(dataDict['value'])
            dNode = self.unconvertNode(dataDict['dot'])
            nNode = self.unconvertNode(dataDict['attr'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.Attribute(value=vNode, dot=dNode, attr=nNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.ASYNCHRONOUS):
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])
            node = cst.Asynchronous(whitespace_after=wANode)
        elif(mNode.nodeType == NodeType.AWAIT):
            eNode = self.unconvertNode(dataDict['expression'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            wAANode = self.unconvertNode(dataDict['whitespaceAfterAwait'])
            node = cst.Await(expression=eNode, lpar=lParNode, rpar=rParNode, whitespace_after_await=wAANode)
        elif(mNode.nodeType == NodeType.YIELD):
            if dataDict['value'] is not None:
                vNode = self.unconvertNode(dataDict['value'])
            else:
                vNode = None
            wAYNode = self.unconvertNode(dataDict['whitespaceAfterYield'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.Yield(value=vNode, whitespace_after_yield=wAYNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.FROM):
            iNode = self.unconvertNode(dataDict['item'])
            wBFNode = self.unconvertNode(dataDict['whitespaceBeforeFrom'])
            wAFNode = self.unconvertNode(dataDict['whitespaceAfterFrom'])
            node = cst.From(item=iNode, whitespace_before_from=wBFNode, whitespace_after_from=wAFNode)
        elif(mNode.nodeType == NodeType.LAMBDA):
            pNode = self.unconvertNode(dataDict['params'])
            bNode = self.unconvertNode(dataDict['body'])
            cNode = self.unconvertNode(dataDict['colon'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            wALNode = self.unconvertNode(dataDict['whitespaceAfterLambda'])
            node = cst.Lambda(params=pNode, body=bNode, colon=cNode, lpar=lParNode, 
                                rpar=rParNode, whitespace_after_lambda=wALNode)
        elif(mNode.nodeType == NodeType.ELLIPSIS):
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.Ellipsis(lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.FLOAT):
            value = mNode.value
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.Float(value=value, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType == NodeType.IMAGINARY):
            value = mNode.value
            lparNode = []
            for n in dataDict['leftParenthesis']:
                lparNode.append(self.unconvertNode(n))
            rparNode = []
            for n in dataDict['rightParenthesis']:
                rparNode.append(self.unconvertNode(n))
            node = cst.Imaginary(value=value, lpar=lparNode, rpar=rparNode)
        elif(mNode.nodeType == NodeType.CONCATENATEDSTRING):
            lNode = self.unconvertNode(dataDict['left'])
            rNode = self.unconvertNode(dataDict['right'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:  
                rParNode.append(self.unconvertNode(n))
            wBNode = self.unconvertNode(dataDict['whitespaceBetween'])
            node = cst.ConcatenatedString(left=lNode, right=rNode, lpar=lParNode, rpar=rParNode, whitespace_between=wBNode)
        elif(mNode.nodeType == NodeType.FORMATTEDSTRING):
            pNode = []
            for n in dataDict['parts']:
                pNode.append(self.unconvertNode(n))
            start = mNode.start
            end = mNode.end
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.FormattedString(parts=pNode, start=start, end=end, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.FORMATTEDSTRINGTEXT):
            value = mNode.value
            node = cst.FormattedStringText(value=value)
        elif(mNode.nodeType == NodeType.FORMATTEDSTRINGEXPRESSION):
            eNode = self.unconverNode(dataDict['expression'])
            if dataDict['conversion'] is not None:
                conversion = dataDict['conversion']
            else:
                conversion = None
            if dataDict['format_spec'] is not None:
                fNode = []
                for n in dataDict['format_spec']:
                    fNode.append(self.unconvertNode(n))
            else:
                fNode = None
            wBENode = self.unconvertNode(dataDict['whitespaceBeforeExpression'])
            wAENode = self.unconvertNode(dataDict['whitespaceAfterExpression'])
            if dataDict['equal'] is not None:
                equalNode = self.unconvertNode(dataDict['equal'])
            else:
                equalNode = None
            node = cst.FormattedStringExpression(expression=eNode, conversion=conversion, format_spec=fNode, whitespace_before_expression=wBENode, whitespace_after_expression=wAENode, equal=equalNode)
        elif(mNode.nodeType == NodeType.TUPLE):
            eNode = []
            for n in dataDict['elements']:
                eNode.append(self.unconvertNode(n))
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.Tuple(elements=eNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.SET):
            eNode = []
            for n in dataDict['elements']:
                eNode.append(self.unconvertNode(n))
            lBNode = self.unconvertNode(dataDict['leftCurlyBrace'])
            rBNode = self.unconvertNode(dataDict['rightCurlyBrace'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.Set(elements=eNode, lcurlybrace=lBNode, rcurlybrace=rBNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.STARREDELEMENT):
            vNode = self.unconvertNode(dataDict['value'])
            cNode = self.unconvertNode(dataDict['comma'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            wBVNode = self.unconvertNode(dataDict['whitespaceBeforeValue'])
            node = cst.StarredElement(value=vNode, comma=cNode, lpar=lParNode, rpar=rParNode, whitespace_before_value=wBVNode)
        elif(mNode.nodeType == NodeType.DICT):
            eNode = []
            for n in dataDict['elements']:
                eNode.append(self.unconvertNode(n))
            lBNode = self.unconvertNode(dataDict['leftCurlyBrace'])
            rBNode = self.unconvertNode(dataDict['rightCurlyBrace'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.Dict(elements=eNode, lcurlybrace=lBNode, rcurlybrace=rBNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.DICTELEMENT):
            kNode = self.unconvertNode(dataDict['key'])
            vNode = self.unconvertNode(dataDict['value'])
            cNode = self.unconvertNode(dataDict['comma'])
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            wACNode = self.unconvertNode(dataDict['whitespaceAfterColon'])
            node = cst.DictElement(key=kNode, value=vNode, comma=cNode, whitespace_before_colon=wBCNode, whitespace_after_colon=wACNode)
        elif(mNode.nodeType == NodeType.STARREDDICTELEMENT):
            vNode = self.unconvertNode(dataDict['value'])
            cNode = self.unconvertNode(dataDict['comma'])
            wBVNode = self.unconvertNode(dataDict['whitespaceBeforeValue'])
            node = cst.StarredDictElement(value=vNode, comma=cNode, whitespace_before_value=wBVNode)
        elif(mNode.nodeType == NodeType.GENERATOREXP):
            eNode = self.unconvertNode(dataDict['elt'])
            fNode = self.unconvertNode(dataDict['forIn'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.GeneratorExp(elt=eNode, for_in=fNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.LISTCOMP):
            eNode = self.unconvertNode(dataDict['elt'])
            fNode = self.unconvertNode(dataDict['forIn'])
            lBNode = self.unconvertNode(dataDict['leftBracket'])
            rBNode = self.unconvertNode(dataDict['rightBracket'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:  
                rParNode.append(self.unconvertNode(n))
            node = cst.ListComp(elt=eNode, for_in=fNode, lbracket=lBNode, rbracket=rBNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.SETCOMP):
            eNode = self.unconvertNode(dataDict['elt'])
            fNode = self.unconvertNode(dataDict['forIn'])
            lBNode = self.unconvertNode(dataDict['leftCurlyBrace'])
            rBNode = self.unconvertNode(dataDict['rightCurlyBrace'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            node = cst.SetComp(elt=eNode, for_in=fNode, lcurlybrace=lBNode, rcurlybrace=rBNode, lpar=lParNode, rpar=rParNode)
        elif(mNode.nodeType == NodeType.DICTCOMP):
            kNode = self.unconvertNode(dataDict['key'])
            vNode = self.unconvertNode(dataDict['value'])
            fNode = self.unconvertNode(dataDict['forIn'])
            lBNode = self.unconvertNode(dataDict['leftCurlyBrace'])
            rBNode = self.unconvertNode(dataDict['rightCurlyBrace'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            wACNode = self.unconvertNode(dataDict['whitespaceAfterColon'])
            node = cst.DictComp(key=kNode, value=vNode, for_in=fNode, lcurlybrace=lBNode, rcurlybrace=rBNode, lpar=lParNode, rpar=rParNode,
                               whitespace_before_colon=wBCNode, whitespace_after_colon=wACNode)
        elif(mNode.nodeType == NodeType.COMPFOR):
            tNode = self.unconvertNode(dataDict['target'])
            iterNode = self.unconvertNode(dataDict['iter'])
            ifNode = []
            for n in dataDict['ifs']:
                ifNode.append(self.unconvertNode(n))
            if dataDict['innerForIn'] is not None:
                innerForInNode = self.unconvertNode(dataDict['innerForIn'])
            else:
                innerForInNode = None
            if dataDict['asynchronous'] is not None:
                asyncNode = self.unconvertNode(dataDict['asynchronous'])
            else:
                asyncNode = None
            wBNode = self.unconvertNode(dataDict['whitespaceBefore'])
            wAFNode = self.unconvertNode(dataDict['whitespaceAfterFor'])
            wBINode = self.unconvertNode(dataDict['whitespaceBeforeIn'])
            wAINode = self.unconvertNode(dataDict['whitespaceAfterIn'])
            node = cst.CompFor(target=tNode, iter=iterNode, ifs=ifNode, inner_for_in=innerForInNode, asynchronous=asyncNode,
                              whitespace_before=wBNode, whitespace_after_for=wAFNode, whitespace_before_in=wBINode, whitespace_after_in=wAINode)
        elif(mNode.nodeType == NodeType.COMPIF):
            tNode = self.unconvertNode(dataDict['test'])
            wBNode = self.unconvertNode(dataDict['whitespaceBefore'])
            wBTNode = self.unconvertNode(dataDict['whitespaceBeforeTest'])
            node = cst.CompIf(test=tNode, whitespace_before=wBNode, whitespace_before_test=wBTNode)
        elif(mNode.nodeType == NodeType.SUBSCRIPT):
            vNode = self.unconvertNode(dataDict['value'])
            sNode = self.unconvertNode(dataDict['slice'])
            lBNode = self.unconvertNode(dataDict['leftBracket'])
            rBNode = self.unconvertNode(dataDict['rightBracket'])
            lParNode = []
            for n in dataDict['leftParenthesis']:
                lParNode.append(self.unconvertNode(n))
            rParNode = []
            for n in dataDict['rightParenthesis']:
                rParNode.append(self.unconvertNode(n))
            wAVNode = self.unconvertNode(dataDict['whitespaceAfterValue'])
            node = cst.Subscript(value=vNode, slice=sNode, lbracket=lBNode, rbracket=rBNode, lpar=lParNode, rpar=rParNode, whitespace_after_value=wAVNode)
        elif(mNode.nodeType == NodeType.INDEX):
            vNode = self.unconvertNode(dataDict['value'])
            if mNode.star is not None:
                star = mNode.star
            else:
                star = None
            wASNode = self.unconvertNode(dataDict['whitespaceAfterStar'])
            node = cst.Index(value=vNode, star=star, whitespace_after_star=wASNode)
        elif(mNode.nodeType == NodeType.SLICE):
            if dataDict['lower'] is not None:
                lNode = self.unconvertNode(dataDict['lower'])
            else:
                lNode = None
            if dataDict['upper'] is not None:
                uNode = self.unconvertNode(dataDict['upper'])
            else:
                uNode = None
            if dataDict['step'] is not None:
                sNode = self.unconvertNode(dataDict['step'])
            else:   
                sNode = None
            fCNode = self.unconvertNode(dataDict['firstColon'])
            sCNode = self.unconvertNode(dataDict['secondColon'])
            node = cst.Slice(lower=lNode, upper=uNode, step=sNode, first_colon=fCNode, second_colon=sCNode)
        elif(mNode.nodeType == NodeType.SUBSCRIPTELEMENT):
            sNode = self.unconvertNode(dataDict['subscript'])
            cNode = self.unconvertNode(dataDict['comma'])
            node = cst.SubscriptElement(subscript=sNode, comma=cNode)
        elif(mNode.nodeType == NodeType.LEFTCURLYBRACE):
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])
            node = cst.LeftCurlyBrace(whitespace_after=wANode)
        elif(mNode.nodeType == NodeType.RIGHTCURLYBRACE):
            wBNode = self.unconvertNode(dataDict['whitespaceBefore'])
            node = cst.RightCurlyBrace(whitespace_before=wBNode)
        elif(mNode.nodeType == NodeType.ANNASSIGN):
            tNode = self.unconvertNode(dataDict['target'])
            aNode = self.unconvertNode(dataDict['annotation'])
            if dataDict['value'] is not None:
                vNode = self.unconvertNode(dataDict['value'])
            else:
                vNode = None
            eNode = self.unconvertNode(dataDict['equal'])
            sCNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.AnnAssign(target=tNode, annotation=aNode, value=vNode, equal=eNode, semicolon=sCNode)
        elif(mNode.nodeType == NodeType.ASSERT):
            tNode = self.unconvertNode(dataDict['test'])
            if dataDict['msg'] is not None:
                mNode = self.unconvertNode(dataDict['msg'])
            else:
                mNode = None
            cNode = self.unconvertNode(dataDict['comma'])
            wAANode = self.unconvertNode(dataDict['whitespaceAfterAssert'])
            sCNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Assert(test=tNode, msg=mNode, comma=cNode, whitespace_after_assert=wAANode, semicolon=sCNode)
        elif(mNode.nodeType == NodeType.BREAK):
            sCNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Break(semicolon=sCNode)
        elif(mNode.nodeType == NodeType.CONTINUE):
            sCNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Continue(semicolon=sCNode)
        elif(mNode.nodeType == NodeType.DEL):
            tNode = self.unconvertNode(dataDict['target'])
            sCNode = self.unconvertNode(dataDict['semicolon'])
            wADNode = self.unconvertNode(dataDict['whitespaceAfterDel'])
            node = cst.Del(target=tNode, semicolon=sCNode, whitespace_after_del=wADNode)
        elif(mNode.nodeType == NodeType.GLOBAL):
            nNode = []
            for n in dataDict['names']:
                nNode.append(self.unconvertNode(n))
            sCNode = self.unconvertNode(dataDict['semicolon'])
            wAGNode = self.unconvertNode(dataDict['whitespaceAfterGlobal'])
            node = cst.Global(names=nNode, semicolon=sCNode, whitespace_after_global=wAGNode)
        elif(mNode.nodeType == NodeType.IMPORT):
            nNode = []
            for n in dataDict['names']:
                nNode.append(self.unconvertNode(n))
            sCNode = self.unconvertNode(dataDict['semicolon'])
            wAINode = self.unconvertNode(dataDict['whitespaceAfterImport'])
            node = cst.Import(names=nNode, semicolon=sCNode, whitespace_after_import=wAINode)
        elif(mNode.nodeType == NodeType.IMPORTFROM):
            if dataDict['module'] is not None:
                mNode = self.unconvertNode(dataDict['module'])
            else:
                mNode = None
            if dataDict['names'] is NodeType.IMPORTSTAR:
                nNode = self.unconvertNode(dataDict['names'])
            else:
                nNode = []
                for n in dataDict['names']:
                    nNode.append(self.unconvertNode(n))
            rNode = []
            for n in dataDict['relative']:
                rNode.append(self.unconvertNode(n))
            if dataDict['leftParenthesis'] is not None:
                lParNode = self.unconvertNode(dataDict['leftParenthesis'])
            else:
                lParNode = None
            if dataDict['rightParenthesis'] is not None:
                rParNode = self.unconvertNode(dataDict['rightParenthesis'])
            else:
                rParNode = None
            sCNode = self.unconvertNode(dataDict['semicolon'])
            wAFNode = self.unconvertNode(dataDict['whitespaceAfterFrom'])
            wAINode = self.unconvertNode(dataDict['whitespaceAfterImport'])
            wBINode = self.unconvertNode(dataDict['whitespaceBeforeImport'])
            node = cst.ImportFrom(module=mNode, names=nNode, relative=rNode, left_parenthesis=lParNode, right_parenthesis=rParNode,
                                 semicolon=sCNode, whitespace_after_from=wAFNode, whitespace_after_import=wAINode,
                                 whitespace_before_import=wBINode)
        elif(mNode.nodeType == NodeType.NONLOCAL):
            nNode = []
            for n in dataDict['names']:
                nNode.append(self.unconvertNode(n))
            sCNode = self.unconvertNode(dataDict['semicolon'])
            wANode = self.unconvertNode(dataDict['whitespaceAfterNonlocal'])
            node = cst.Nonlocal(names=nNode, semicolon=sCNode, whitespace_after_nonlocal=wANode)
        elif(mNode.nodeType == NodeType.PASS):
            sCNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Pass(semicolon=sCNode)
        elif(mNode.nodeType == NodeType.RAISE):
            if dataDict['exc'] is not None:
                eNode = self.unconvertNode(dataDict['exc'])
            else:
                eNode = None
            if dataDict['cause'] is not None:
                cNode = self.unconvertNode(dataDict['cause'])
            else:
                cNode = None
            wARNode = self.unconvertNode(dataDict['whitespaceAfterRaise'])
            sCNode = self.unconvertNode(dataDict['semicolon'])
            node = cst.Raise(exc=eNode, cause=cNode, whitespace_after_raise=wARNode, whitespace_before_cause=wBCNode, semicolon=sCNode)
        elif(mNode.nodeType == NodeType.TRY):
            bNode = self.unconvertNode(dataDict['body'])
            hNode = []
            for n in dataDict['handlers']:
                hNode.append(self.unconvertNode(n))
            if dataDict['orelse'] is not None:
                oNode = self.unconvertNode(dataDict['orelse'])
            else:
                oNode = None
            if dataDict['finalbody'] is not None:
                fNode = self.unconvertNode(dataDict['finalbody'])
            else:
                fNode = None
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.Try(body=bNode, handlers=hNode, orelse=oNode, finalbody=fNode, leading_lines=lLNode, whitespace_before_colon=wBCNode)
        elif(mNode.nodeType == NodeType.WHILE):
            tNode = self.unconvertNode(dataDict['test'])
            bNode = self.unconvertNode(dataDict['body'])
            if dataDict['orelse'] is not None:
                oNode = self.unconvertNode(dataDict['orelse'])
            else:
                oNode = None
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wAWNode = self.unconvertNode(dataDict['whitespaceAfterWhile'])
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.While(test=tNode, body=bNode, orelse=oNode, leading_lines=lLNode, whitespace_after_while=wAWNode, whitespace_before_colon=wBCNode)
        elif(mNode.nodeType == NodeType.WITH):
            iNode = []
            for n in dataDict['items']:
                iNode.append(self.unconvertNode(n))
            bNode = self.unconvertNode(dataDict['body'])
            if dataDict['asynchronous'] is not None:
                aNode = self.unconvertNode(dataDict['asynchronous'])
            else:
                aNode = None
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            lParNode = self.unconvertNode(dataDict['leftParenthesis'])
            rParNode = self.unconvertNode(dataDict['rightParenthesis'])
            wAWNode = self.unconvertNode(dataDict['whitespaceAfterWith'])
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.With(items=iNode, body=bNode, asynchronous=aNode, leading_lines=lLNode, lpar=lParNode, rpar=rParNode, whitespace_after_with=wAWNode, whitespace_before_colon=wBCNode)
        elif(mNode.nodeType == NodeType.ASNAME):
            nNode = self.unconvertNode(dataDict['name'])
            wBANode = self.unconvertNode(dataDict['whitespaceBeforeAs'])
            wAANode = self.unconvertNode(dataDict['whitespaceAfterAs'])
            node = cst.AsName(name=nNode, whitespace_before_as=wBANode, whitespace_after_as=wAANode)
        elif(mNode.nodeType == NodeType.DECORATOR):
            dNode = self.unconvertNode(dataDict['decorator'])
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wAANode = self.unconvertNode(dataDict['whitespaceAfterAt'])
            tWNode = self.unconvertNode(dataDict['trailingWhitespace'])
            node = cst.Decorator(decorator=dNode, leading_lines=lLNode, whitespace_after_at=wAANode, trailing_whitespace=tWNode)
        elif(mNode.nodeType == NodeType.EXCEPTHANDLER):
            bNode = self.unconvertNode(dataDict['body'])
            if dataDict['type'] is not None:
                tNode = self.unconvertNode(dataDict['type'])
            else:
                tNode = None
            if dataDict['name'] is not None:
                nNode = self.unconvertNode(dataDict['name'])
            else:
                nNode = None
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wAENode = self.unconvertNode(dataDict['whitespaceAfterExcept'])
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.ExceptHandler(body=bNode, type=tNode, name=nNode, leading_lines=lLNode, whitespace_after_except=wAENode, whitespace_before_colon=wBCNode)
        elif(mNode.nodeType == NodeType.FINALLY):
            bNode = self.unconvertNode(dataDict['body'])
            lLNode = []
            for n in dataDict['leadingLines']:
                lLNode.append(self.unconvertNode(n))
            wBCNode = self.unconvertNode(dataDict['whitespaceBeforeColon'])
            node = cst.Finally(body=bNode, leading_lines=lLNode, whitespace_before_colon=wBCNode)
        elif(mNode.nodeType == NodeType.IMPORTALIAS):
            nNode = self.unconvertNode(dataDict['name'])
            if dataDict['asname'] is not None:
                aNode = self.unconvertNode(dataDict['asname'])
            else:
                aNode = None
            cNode = self.unconvertNode(dataDict['comma'])
            node = cst.ImportAlias(name=nNode, asname=aNode, comma=cNode)
        elif(mNode.nodeType == NodeType.NAMEITEM):
            nNode = self.unconvertNode(dataDict['name'])
            cNode = self.unconvertNode(dataDict['comma'])
            node = cst.NameItem(name=nNode, comma=cNode)
        elif(mNode.nodeType == NodeType.PARAMSLASH):
            cNode = self.unconvertNode(dataDict['comma'])
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])
            node = cst.ParamsSlash(comma=cNode, whitespace_after=wANode)
        elif(mNode.nodeType == NodeType.WITHITEM):
            iNode = self.unconvertNode(dataDict['item'])
            if dataDict['asname'] is not None:
                aNode = self.unconvertNode(dataDict['asname'])
            else:
                aNode = None
            cNode = self.unconvertNode(dataDict['comma'])
            node = cst.WithItem(item=iNode, asname=aNode, comma=cNode)
        elif(mNode.nodeType == NodeType.SIMPLESTATEMENTSUITE):
            bNode = []
            for n in dataDict['body']:
                bNode.append(self.unconvertNode(n))
            lWNode = self.unconvertNode(dataDict['leadingWhitespace'])
            tWNode = self.unconvertNode(dataDict['trailingWhitespace'])
            node = cst.SimpleStatementSuite(body=bNode, leading_whitespace=lWNode, trailing_whitespace=tWNode)
        elif(mNode.nodeType == NodeType.DOT):
            wBNode = self.unconvertNode(dataDict['whitespaceBefore'])
            wANode = self.unconvertNode(dataDict['whitespaceAfter'])
            node = cst.Dot(whitespace_before=wBNode, whitespace_after=wANode)
        elif(mNode.nodeType == NodeType.PARENTHESIZEDWHITESPACE):
            fLNode = self.unconvertNode(dataDict['firstLine'])
            eLNode = []
            for n in dataDict['emptyLines']:
                eLNode.append(self.unconvertNode(n))
            indent = mNode.indent
            lLNode = self.unconvertNode(dataDict['lastLine'])
            node = cst.ParenthesizedWhitespace(first_line=fLNode, empty_lines=eLNode, indent=indent, last_line=lLNode)
        else:
            raise ValueError(f"Unknown node type: {mNode.nodeType}")

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
    