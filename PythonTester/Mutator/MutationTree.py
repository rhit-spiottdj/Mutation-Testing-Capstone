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
    children = None
    parent = None
    nodeType = None
    flagToExclude = False
    rowNumber = -1
    colNumber = -1
    value = None

    def __init__(self, nodeType, value = None, children = None):
        self.children = children
        self.value = value
        self.nodeType = nodeType

    def attachChildren(self, nodes):
        self.children = nodes
    
    def excludeNode(self):
        self.flagToExclude = True

    def includeNode(self):
        self.flagToExclude = False