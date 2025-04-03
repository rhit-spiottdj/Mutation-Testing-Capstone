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
        # print("Old curNode: " + str(self.currentNode))
        print("\nOld curNode type: " + str(self.currentNode.nodeType))
        if(not self.currentNode.flagToExclude):
            for node in self.currentNode.children:
                if(node is not None):
                    # if(not isinstance(node, list) or (isinstance(node, list) and not node))
                    if isinstance(node, MutationNode):
                        # print("Iterating over child node: " + str(node) + "\t" + str(node.nodeType))
                        print("Iterating over child node: " + str(node.nodeType))
                        self.queue.put(node)
                    else:
                        # if (isinstance(node, list)):
                            # print("The 'node' is a list")
                        for actualNode in node:
                            # print("Iterating over child nodes: " + str(actualNode) + "\t" + str(actualNode.nodeType))
                            print("Iterating over child nodes: " + str(actualNode.nodeType))
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
    mutateMe = False

    def __init__(self, nodeType, rowNumber, colNumber, dataDict, value = None, children = None, parent = None, mutateMe = False):
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
        self.mutateMe = mutateMe

    def attachChildren(self, nodes):
        self.children = nodes
        # print("Attached children: " + str(self.children))
        for node in nodes:
            if isinstance(node, MutationNode):
                node.parent = self
            else:
                if (node is None):
                    continue
                for actualNode in node:
                    if isinstance(actualNode, MutationNode):
                        actualNode.parent = self
    
    def excludeNode(self):
        self.flagToExclude = True

    def includeNode(self):
        self.flagToExclude = False