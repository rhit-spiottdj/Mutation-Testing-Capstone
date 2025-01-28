import os
import libcst as cst

from libcst.display import dump

# List of nodes linked with list of single mutations before mutation
global_nodes = []
global_line_nums = []
global_col_nums = []
global_line_num = -1
global_col_num = -1
mutation_map = {
    "Add()" : cst.Subtract(),
    "AddAssign()" : cst.SubtractAssign(),
    "Subtract()" : cst.Add(),
    "SubtractAssign()" : cst.AddAssign(),
    "Multiply()" : cst.Divide(),
    "MultiplyAssign()" : cst.DivideAssign(),
    "Divide()" : cst.Multiply(),
    "DivideAssign()" : cst.MultiplyAssign(),
    "Modulo()" : cst.Multiply(),
    "ModuloAssign()" : cst.MultiplyAssign(),
    "BitAnd()" : cst.BitOr(),
    "BitOr()" : cst.BitAnd(),
}

class MutationTree:
    # List of Individual mutations
    mutations = []

    og_tree = None
    tree = None

    original_code = ""
    C = ""
    file_path = ""
    # List of nodes linked with list of single mutations before mutation
    nodes = []
    line_nums = []
    col_nums = []
    
    def __init__(self, fs):
        # global tree, og_tree
        # VERY IMPORTANT STEP!!!!!
        # Establish path to original file
        self.C = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.file_path = fs

        with open(self.C + self.file_path, 'r', encoding='utf-8') as fd:
            self.original_code = fd.read()
            fd.close()
            self.tree = cst.parse_module(self.original_code)

            self.og_tree = self.tree
            
            # Important to print out the syntax of node tree
            # print("\n", dump(self.tree)) ##Used for understanding utilization of ast methods

            self.metaDataVisitor = None
            self.visitor = VisitNodes()
            self.mutator = MutateNodes()

    def loadMutatedCode(self, i):
        with open(self.C + self.file_path, 'w', encoding='utf-8') as fd:
            fd.write(self.mutations[i])
            fd.flush()
            fd.close()
            self.tree = cst.parse_module(self.mutations[i])

    def loadOriginalCode(self):
        with open(self.C + self.file_path, 'w', encoding='utf-8') as fd:
            fd.write(self.original_code)
            fd.flush()
            fd.close()

    def traverseTree(self):
        global global_line_nums, global_col_nums, global_nodes
        global_line_nums = []
        global_col_nums = []
        global_nodes = []
        self.metaDataVisitor = cst.MetadataWrapper(self.tree)
        self.metaDataVisitor.visit(self.visitor)
        self.line_nums = global_line_nums
        self.col_nums = global_col_nums
        self.nodes = global_nodes

    def retLineNum(self):
        return self.line_nums
    
    def retColNum(self):
        return self.col_nums
    
    def retNodes(self):
        return self.nodes

    def retOriginalCode(self):
        return self.original_code
    
    def retMutations(self):
        return self.mutations
    
    def retMutationLength(self):
        return len(self.mutations)
    
    def retTree(self):
        return self.tree

    def basicMutateTree(self):
        global global_line_num, global_col_num
        self.mutations = []
        self.traverseTree()
        for var in range(len(self.nodes)):
            global_line_num = self.line_nums[var]
            global_col_num = self.col_nums[var]
            self.metaDataVisitor = cst.MetadataWrapper(self.tree)
            new_tree = self.metaDataVisitor.visit(self.mutator)
            self.mutations.append(new_tree.code)


# def main(code):
#     tree = MutationTree(code)
#     tree.traverseTree()

class VisitNodes(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)
    global global_line_nums, global_col_nums, global_nodes

    def visit_BinaryOperation(self, node):
        pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start
        global_line_nums.append(pos.line)
        global_col_nums.append(pos.column)
        global_nodes.append(dump(node.operator))

    def visit_AugAssign(self, node):
        pos = self.get_metadata(cst.metadata.PositionProvider, node.operator).start
        global_line_nums.append(pos.line)
        global_col_nums.append(pos.column)
        global_nodes.append(dump(node.operator))

class MutateNodes(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)
    
    def leave_BinaryOperation(self, original_node, updated_node):
        pos = self.get_metadata(cst.metadata.PositionProvider, original_node.operator).start
        if global_line_num == pos.line and global_col_num == pos.column:
            new_node = updated_node.with_changes(
                operator = mutation_map[dump(original_node.operator)]
            )
            return new_node
        return updated_node
    
    def leave_AugAssign(self, original_node, updated_node):
        pos = self.get_metadata(cst.metadata.PositionProvider, original_node.operator).start
        if global_line_num == pos.line and global_col_num == pos.column:
            new_node = updated_node.with_changes(
                operator = mutation_map[dump(original_node.operator)]
            )
            return new_node
        return updated_node
