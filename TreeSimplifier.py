import ast

class TreeSimplifier(ast.NodeVisitor):
    def __init__(self):
        self.simple_tree = {"ClassDef": [], "FunctionDef": []}

    def visit_ClassDef(self, node):
        self.simple_tree["ClassDef"].append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.simple_tree["FunctionDef"].append(node.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.simple_tree)
    