import ast
import os
import sys

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from generator.CodeAnalyzer import CodeAnalyzer
from generator.CodeGenerator import CodeGenerator


class FileGenerator:
    def __init__(self, conf: dict, root_name: str, filepath: str) -> None:

        self.conf: dict = conf
        self.root_name: str = root_name
        self.filepath: str = filepath
        self.testpath: str = FileGenerator._get_out_path(root_name, filepath)

    def _get_out_path(root_name: str, filepath: str) -> str:

        name = os.path.split(filepath)[1]

        # if generating for a single file
        if name == root_name:
            result = ".\\test_" + name
        else:
            result = filepath.replace(root_name, "test_" + root_name).replace(name, "test_" + name)

        return result

    def generate_file(self):

        # if file already exists avoid overwrite
        if os.path.exists(self.testpath):
            print(self.testpath[2:] + " already exists. Avoiding overwrite")

        else:

            print(f"Creating test script for: { self.filepath[2:] }")

            # if route does not exist create it
            os.makedirs(os.path.split(self.testpath)[0], exist_ok=True)

            # create ast from source file
            with open(self.filepath, "r") as source:
                tree = ast.parse(source.read())

            # get the necessary details from the tree
            analyzer = CodeAnalyzer()
            analyzer.visit(tree)
            code_dict = analyzer.code_dict

            # create test file code from code details
            tcg = CodeGenerator(self.conf, self.filepath, code_dict)
            tcg.generate_full()
            test_code = tcg.get_test_code()

            # write code to output file
            with open(self.testpath, "w") as out:
                out.write(test_code)
