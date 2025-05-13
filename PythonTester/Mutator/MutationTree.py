from queue import Queue

class MutationTree:

    headNode = None
    currentNode = None
    mutatedNode = None
    # methodsToExclude = None
    queue = None


    def __init__(self, node):
        # create the actual tree here from a set of nodes? idk
        self.headNode = node
        self.currentNode = node
        self.queue = Queue()

    def nextNode(self):
        # print("\nOld curNode type: " + str(self.currentNode.nodeType))
        if(not self.currentNode.flagToExclude):
            for node in self.currentNode.children:
                if(node is not None):
                    if isinstance(node, MutationNode):
                        # print("Iterating over child node: \t" + str(node.nodeType))
                        self.queue.put(node)
                    else:
                        for actualNode in node:
                            # print("Iterating over child nodes: \t" + str(actualNode.nodeType))
                            if isinstance(actualNode, MutationNode):
                                self.queue.put(actualNode)
        if(not self.queue.empty()):
            self.currentNode = self.queue.get()
            return True
        return False

    def retCurNode(self):
        return self.currentNode
    
    def setMutatedNode(self):
        self.mutatedNode = self.currentNode

class MutationNode:
    nodeType = None
    value = None
    children = []
    parent = None
    flagToExclude = False
    rowNumber = None
    colNumber = None
    dataDict = {}
    isMutated = False
    oldType = None
    method_name = None

    def __init__(self, nodeType, rowNumber, colNumber, dataDict, value = None, children = None, parent = None, isMutated = False, method_name = None):
        self.nodeType = nodeType
        self.value = value
        if (children):
            self.children = children
        else:
            self.children = []
        self.parent = parent
        self.rowNumber = rowNumber
        self.colNumber = colNumber
        self.dataDict = dataDict
        self.isMutated = isMutated
        self.method_name = method_name

    def attachChildren(self, nodes):
        self.children = nodes
        for node in nodes:
            if isinstance(node, MutationNode):
                node.parent = self
            else:
                if (node is None):
                    continue
                for actualNode in node:
                    if isinstance(actualNode, MutationNode):
                        actualNode.parent = self
    
    def attachOneChild(self, node):
        if isinstance(node, MutationNode):
            self.children.append(node)
            node.parent = self
    
    def excludeNode(self):
        self.flagToExclude = True

    def includeNode(self):
        self.flagToExclude = False

    def setOldType(self, type):
        self.oldType = type

    # For Display to User what the Node is
    def toString(self):
        nodeString = "\nMutant: \n" + "Original Type: " + str(self.oldType) + "\nNew Type: " + str(self.nodeType) + "\nCol: " + str(self.colNumber) + "\nRow: " + str(self.rowNumber) + "\n"
        if(self.value is not None):
            nodeString += "Value: " + str(self.value) + "\n"

        return nodeString