import ast
from TreeSimplifier import TreeSimplifier


class TestTemplateGenerator:

    def __init__(self) -> None:
        self.tree = None
        self.simple_tree = None

    def generate_tree(self, filepath: str) -> None:
        with open( filepath, 'r') as source:
            self.tree = ast.parse(source.read())
        
        simplifier = TreeSimplifier()
        simplifier.visit(self.tree)
        self.simple_tree = simplifier.simple_tree

    def generate_test_case(self, SUT) -> str:
        '''Create a test case function for a given SUT'''

        test_string = f"def test_{SUT}():\n\tassert True\n\n"
        return test_string
    
    def write_test_file(self, root, filename, filepath: str) -> None:

        self.generate_tree(filepath)

        test_path = filepath.replace( root , "test_" + root ).replace(filename, "test_" + filename) # pretty horrible, should be done elsewhere

        with open( test_path, 'a') as test_file:
            for key in self.simple_tree.keys():
                for syn in self.simple_tree[key]:
                    test_file.write(self.generate_test_case(syn))

    def dump_tree(self) -> None:
        if self.tree:
            print(ast.dump(self.tree, indent=4))
        else:
            print("No tree has been generated.")