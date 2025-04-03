import copy

class TreeMutator:
    tree = None
    mutants = []

    def generateMutations(self, tree, params):
        self.tree = tree

        mutationMap = params # Would get map from params

        self.checkForMutation(mutationMap)
        while self.tree.nextNode(): 
          self.checkForMutation(mutationMap)
        
        return self.mutants
    
    def checkForMutation(self, mutationMap):
        print('\nCurrent Node: ' + str(self.tree.retCurNode().nodeType)) #debug
        # print('Current Node Children: ' + str(self.tree.retCurNode().children) + '\n') #debug
        temp = self.tree.retCurNode().children
        children = []
        for x in temp:
            if not x:
                    children.append([])
            else:
                if isinstance(x, list):
                    children.append(x[0].nodeType.name)
                else:
                    children.append(x.nodeType.name)
        print('Current Node Children Types: ' + str(children)) #debug

        if(self.tree.retCurNode().nodeType in mutationMap):
            deepCopy = copy.deepcopy(self.tree)
            deepCopy.retCurNode().nodeType = mutationMap[deepCopy.retCurNode().nodeType]
            deepCopy.setMutatedNode()
            self.mutants.append(deepCopy)
