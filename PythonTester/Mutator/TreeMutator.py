from Mutator.MutationTree import MutationNode
from Mutator.NodeTypes import NodeType
class TreeMutator:
    tree = None
    mutants = []
    ogNode = None
    index = 0

    def generateMutations(self, tree, params):
        self.tree = tree

        mutationMap = params # Would get map from params

        if (self.tree.currentNode.isMutated):
            curNode = self.tree.retCurNode()
            curNode.nodeType = self.ogNode.nodeType
    
        foundMutant = self.checkForMutation(mutationMap)
        while not foundMutant and self.tree.nextNode(): 
            foundMutant = self.checkForMutation(mutationMap)
        
        if(not foundMutant):
            return None
        return self.tree
    
    def checkForMutation(self, mutationMap):
        curNode = self.tree.retCurNode()
        # print('\nCurrent Node: ' + str(curNode.nodeType)) #debug
        # print('Current Node Children: ' + str(self.tree.retCurNode().children) + '\n') #debug
        # temp = curNode.children
        # children = []
        # for x in temp:
        #     if not x:
        #             children.append([])
        #     else:
        #         if isinstance(x, list):
        #             children.append(x[0].nodeType.name)
        #         else:
        #             children.append(x.nodeType.name)
        # print('Current Node Children Types: ' + str(children)) #debug

        if(curNode.nodeType in mutationMap):
            self.ogNode = MutationNode(curNode.nodeType, curNode.rowNumber, curNode.colNumber, curNode.dataDict, curNode.value, curNode.children, curNode.parent, False)
            mutations = mutationMap[curNode.nodeType] # the line doing the actual mutation
            if(isinstance(mutations, list)):
                if(self.index < len(mutations)):
                    if(curNode.nodeType == NodeType.IF or curNode.nodeType == NodeType.ELSE):
                        oldBool = curNode.dataDict['test']
                        newBool = None
                        if(mutations[self.index] == NodeType.TRUE):
                            newBool = MutationNode(mutations[self.index], oldBool.rowNumber, oldBool.colNumber, {}, value = 'True')
                        elif(mutations[self.index] == NodeType.FALSE):
                            newBool = MutationNode(mutations[self.index], oldBool.rowNumber, oldBool.colNumber, {}, value = 'False')
                        curNode.dataDict['test'] = newBool
                        curNode.attachOneChild(newBool)
                    else:   
                        curNode.nodeType = mutations[self.index] 
                    curNode.isMutated = True
                    self.index += 1
                else:
                    self.index = 0
                    curNode.isMutated = False
                    return False
            elif(not curNode.isMutated):
                curNode.isMutated = True
                curNode.nodeType = mutations
            else:
                self.index = 0
                curNode.isMutated = False
                return False
            return True
        self.index = 0
        curNode.isMutated = False
        return False