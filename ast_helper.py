import ast

code = """
def get_age(self):
    return self.age
"""

tree = ast.parse(code)
print(ast.dump(tree, indent=4))
print(tree.body[0].body[0].targets)