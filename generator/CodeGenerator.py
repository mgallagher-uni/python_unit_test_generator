import ast
from typing import Optional

from pprint import pprint


class CodeGenerator:
    def __init__(self, code_dict) -> None:
        self.code_dict = code_dict
        self.test_code = ""

    def generate_full(self):

        # generate imports
        self.test_code += "import pytest\n\n"

        for class_info in self.code_dict["classes"].items():
            self.test_code += CodeGenerator._generate_fixture_function(class_info)

        for _class in self.code_dict["classes"].keys():
            for meth_info in self.code_dict["classes"][_class]["methods"].items():
                self.test_code += CodeGenerator._generate_test_case(meth_info, _class)

        for func_info in self.code_dict["functions"].items():
            self.test_code += CodeGenerator._generate_test_case(func_info)

    def _generate_fixture_function(class_info: tuple) -> str:

        fixture_name = "temp_to_do"
        class_init = CodeGenerator._generate_class_initialisation(class_info)

        code_string = (
            f"@pytest.fixture\ndef { fixture_name }():\n"
            + "\treturn "
            + class_init
            + "\n"
            + "\n"
        )

        return code_string

    def _generate_class_initialisation(class_info: tuple) -> str:

        class_name = class_info[0]
        params = class_info[1]["params"]

        # param_names, param_types = zip(*params)

        # code_string = f"{class_name.lower()} = {class_name}( { params } )\n"

        return class_name + f"( { params } )"

    def _generate_test_case(func_info: tuple, class_name: Optional[str] = None) -> str:
        """Create a test case for a given function"""

        # if function is a class's method

        if class_name:
            func_name = (
                class_name.lower() + "_" + func_info[0]
            )  # this is necessary for duplicate names from seperate classes
        else:
            func_name = func_info[
                0
            ]  # look to remove when only one class present, or no clashes perhaps

        params = func_info[1]["params"]
        returns = func_info[1]["returns"]

        test_string = f"def test_{func_name}():\n\tassert True\n\n"
        return test_string

    def get_test_code(self) -> str:
        return self.test_code

    def report(self) -> None:
        print(self.test_code)
