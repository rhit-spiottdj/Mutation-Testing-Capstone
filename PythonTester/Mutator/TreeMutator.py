class TreeMutator:
    og_tree = None
    tree = None
    mutants = []

    def generateMutations(self, tree, param):
        self.tree = tree
        self.og_tree = tree

        self.checkForMutation(param)
        while self.tree.nextNode() and self.og_tree.nextNode():
          self.checkForMutation(param)
        
        return self.mutants
    
    def checkForMutation(self, param):
        print('Current Node: ' + str(self.tree.retCurNode().nodeType) + '\n') #debug
        if param[self.tree.retCurNode().nodeType] is not None:
            self.tree.retCurNode().nodeType = param[self.tree.retCurNode().nodeType]
            self.tree.setMutatedNode()
            self.mutants.append(self.tree)
            self.tree = self.og_tree 
