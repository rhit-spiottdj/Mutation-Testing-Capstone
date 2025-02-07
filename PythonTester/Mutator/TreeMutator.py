class TreeMutator:
    og_tree = None
    tree = None
    mutants = []

    def __init__(self):
        return

    def generateMutations(self, tree, param):
        self.tree = tree
        self.og_tree = tree

        self.checkForMutation(param)
        while self.tree.nextNode() and self.og_tree.nextNode():
          self.checkForMutation(param)
        
        return self.mutants
    
    def checkForMutation(self, param):
        if param[self.tree.retCurNode().nodeType] != None:
            self.tree.retCurNode().nodeType = param[self.tree.retCurNode().nodeType]
            self.tree.setMutatedNode()
            self.mutants.append(self.tree)
            self.tree = self.og_tree 
