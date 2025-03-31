class TreeMutator:
    og_tree = None
    tree = None
    mutants = []

    def generateMutations(self, tree, params):
        self.tree = tree
        self.og_tree = tree

        mutationMap = params # Would get map from params

        self.checkForMutation(mutationMap)
        while self.tree.nextNode() and self.og_tree.nextNode():
          self.checkForMutation(mutationMap)
        
        return self.mutants
    
    def checkForMutation(self, mutationMap):
        print('Current Node: ' + str(self.tree.retCurNode().nodeType)) #debug
        print('Current Node Children: ' + str(self.tree.retCurNode().children) + '\n') #debug
        if(self.tree.retCurNode().nodeType in mutationMap):
            self.tree.retCurNode().nodeType = mutationMap[self.tree.retCurNode().nodeType]
            self.tree.setMutatedNode()
            self.mutants.append(self.tree)
            self.tree = self.og_tree 
