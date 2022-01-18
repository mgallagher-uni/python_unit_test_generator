import os
import sys
import ast

class TestSuiteGenerator:

    def __init__(self):

        self.prefix = "test_"

        if len(sys.argv) == 1:
            print("No directory given")
            exit(0)
        else:
            self.root_dir = str(sys.argv[1])

        self.filepath: str
        self.testpath: str
        

    def get_dir_object(self, dir_name: str) -> os.DirEntry:
        '''Given the name of the directory find the os.DirEntry object'''
        temp_ents = os.scandir()
        for te in temp_ents:
            if te.name == dir_name:
                temp_ents.close()
                return te

    def traverse_directory(self, ent: os.DirEntry) -> None:
        '''Traverses through given directory creating corresponding test files in test directory.'''

        directory = os.scandir(ent.path)
        for sub_ent in directory:
            if sub_ent.is_dir():
                self.traverse_directory(sub_ent)
            elif sub_ent.name.endswith(".py"):
                self.filepath = sub_ent.path
                self.create_test_file()
        directory.close()


    def create_test_file(self) -> None:
        '''Create a test file for a python module in the corresponding folder in the test directory.'''

        # get output testpath from filepath
        name = os.path.split(self.filepath)[1]
        self.testpath = self.filepath.replace( self.root_dir, self.prefix + self.root_dir ).replace( name, self.prefix + name )

        # if route does not exist create it
        os.makedirs(os.path.split(self.testpath)[0], exist_ok=True)

        # if file does not already exist
        if not os.path.exists(self.testpath):
            # create the test file in the corresponding location
            self.write_test_file()


    def generate_tree(self) -> dict:
        '''Creates a model of an AST from a .py file'''

        with open( self.filepath, 'r') as source:
            tree = ast.parse(source.read())
        
        analyzer = TreeAnalyzer()
        analyzer.visit(tree)
        return analyzer.tree_dict


    def generate_test_case(self, SUT) -> str:
        '''Create a test case function for a given SUT'''

        test_string = f"def test_{SUT}():\n\tassert True\n\n"
        return test_string
    

    def write_test_file(self) -> None:

        tree_dict = self.generate_tree()

        with open( self.testpath, 'a') as test_file:
            for key in tree_dict.keys():
                for syn in tree_dict[key]:
                    test_file.write(self.generate_test_case(syn))

    def generate(self) -> None:
        self.traverse_directory(self.get_dir_object(self.root_dir))

    

class TreeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.tree_dict = {"ClassDef": [], "FunctionDef": []}

    def visit_ClassDef(self, node):
        self.tree_dict["ClassDef"].append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.tree_dict["FunctionDef"].append(node.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.tree_dict)
    


if __name__ == "__main__":
    TestSuiteGenerator().generate()