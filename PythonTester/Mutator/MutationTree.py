import queue

class MutationTree:

    headNode = None
    currentNode = None
    mutatedNode = None
    # methodsToExclude = None
    queue = []


    def __init__(self, node):
        # create the actual tree here from a set of nodes? idk
        self.headNode = node
        self.currentNode = node
        

    def nextNode(self):
        if(self.currentNode.children is not None and not self.currentNode.flagToExclude):
            for node in self.currentNode.children:
                self.queue.append(node)
        if(self.queue is not None):
            self.currentNode = self.queue.pop(0)
            return True
        return False

    def retCurNode(self):
        return self.currentNode
    
    def setMutatedNode(self):
        self.mutatedNode = self.currentNode

class MutationNode:
    nodeType = None
    value = None
    children = None
    parent = None
    flagToExclude = False
    rowNumber = None
    colNumber = None
    dataDict = {}

    def __init__(self, nodeType, rowNumber, colNumber, dataDict, value = None, children = None, parent = None):
        self.nodeType = nodeType
        self.value = value
        self.children = children
        self.parent = parent
        self.rowNumber = rowNumber
        self.colNumber = colNumber
        self.dataDict = dataDict

    def attachChildren(self, nodes):
        self.children = nodes
        for node in nodes:
            node.parent = self
    
    def excludeNode(self):
        self.flagToExclude = True

    def includeNode(self):
        self.flagToExclude = False