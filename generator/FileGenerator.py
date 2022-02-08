import ast
import os

from CodeAnalyzer import CodeAnalyzer
from CodeGenerator import CodeGenerator


class FileGenerator:
    def __init__(self, root_dir: str, filepath: str) -> None:
        self.root_dir = root_dir
        self.filepath = filepath
        self.testpath = FileGenerator._get_out_path(root_dir, filepath)

    def _get_out_path(root_dir: str, filepath: str) -> str:
        name = os.path.split(filepath)[1]
        return filepath.replace(root_dir, "test_" + root_dir).replace(
            name, "test_" + name
        )

    def generate_file(self):

        # if file already exists avoid overwrite
        if os.path.exists(self.testpath):
            print(self.testpath + " already exists. Avoiding overwrite")

        else:
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
            tcg = CodeGenerator(code_dict)
            tcg.generate_full()
            test_code = tcg.get_test_code()

            # write code to output file
            with open(self.testpath, "w") as out:
                out.write(test_code)
