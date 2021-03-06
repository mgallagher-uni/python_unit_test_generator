import ast
from typing import Optional
from pprint import pprint


class CodeGenerator:
    def __init__(self, conf: dict, filepath: str, code_dict: dict) -> None:

        self.filepath = filepath
        self.code_dict = code_dict
        self.unique_functions = self.check_unique_function_names()
        self.setters_getters: bool = conf["setters_getters"]
        self.test_code = ""

    def generate_full(self):

        # generate imports
        self.test_code += "import pytest\n"

        self.test_code += self.generate_import()

        if self.code_dict["classes"]:

            for class_info in self.code_dict["classes"].items():
                self.test_code += self.generate_fixture_function(class_info)

            for _class in self.code_dict["classes"].keys():
                for meth_info in self.code_dict["classes"][_class]["methods"].items():
                    self.test_code += self.generate_test_case(meth_info, _class)

            if self.setters_getters:
                for set_info in self.code_dict["classes"][_class]["setters"].items():
                    self.test_code += "# IT's a SeTTEer\n"
                    self.test_code += self.generate_test_case(set_info, _class)

                for get_info in self.code_dict["classes"][_class]["getters"].items():
                    self.test_code += "# IT's a GeTTEer\n"
                    self.test_code += self.generate_test_case(get_info, _class)


        for func_info in self.code_dict["functions"].items():
            self.test_code += self.generate_test_case(func_info)

    def check_unique_function_names(self):

        names = []

        for class_ in self.code_dict["classes"].keys():
            for method in self.code_dict["classes"][class_]["methods"].keys():
                names.append(method)
        for func in self.code_dict["functions"].keys():
            names.append(func)

        return len(names) == len(set(names))

    def generate_import(self):

        import_path = ".".join(self.filepath[:-3].split("\\")[1:])
        code_string = f"from { import_path } import " + "*"

        # ", ".join(list(self.code_dict["classes"].keys()))

        # if len(self.code_dict["functions"].keys()) != 0:
        #     code_string += ", ".join(list(self.code_dict["functions"].keys()))

        code_string += "\n\n"

        return code_string

    def generate_fixture_function(self, class_info: tuple) -> str:

        fixture_name = "temp_to_do"
        class_init = self.generate_class_initialisation(class_info)

        code_string = (
            f"@pytest.fixture\ndef { fixture_name }():\n"
            + "\treturn "
            + class_init
            + "\n"
            + "\n"
        )

        return code_string

    def generate_class_initialisation(self, class_info: tuple) -> str:

        class_name = class_info[0]
        params = class_info[1]["params"]

        # param_names, param_types = zip(*params)

        # code_string = f"{class_name.lower()} = {class_name}( { params } )\n"

        return class_name + f"( { params } )"

    def generate_test_case(
        self, func_info: tuple, class_name: Optional[str] = None
    ) -> str:
        """Create a test case for a given function"""

        # if function is a class's method
        if class_name and not self.unique_functions:
            func_name = class_name.lower() + "_" + func_info[0]
        else:
            func_name = func_info[0]

        params = func_info[1]["params"]
        returns = func_info[1]["returns"]

        test_string = f"def test_{func_name}():\n\tassert True\n\n"
        return test_string

    def get_test_code(self) -> str:
        return self.test_code

    def report(self) -> None:
        print(self.test_code)
