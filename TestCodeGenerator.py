import ast
from CodeAnalyzer import CodeAnalyzer


class TestCodeGenerator:
    def __init__(self) -> None:

        self.test_code = ""

    def _generate_fixture_function(class_info):

        func_name = "temp_to_do"
        code_string = (
            f"@pytest.fixture\ndef { func_name }():\n\t"
            + TestCodeGenerator._generate_class_initialisation(class_info)
            + "\n"
        )

        return code_string

    def _generate_class_initialisation(class_info: tuple) -> str:

        class_name = class_info[0]
        params = class_info[1]["params"]

        param_names, param_types = zip(*params)

        #code_string = f"{class_name.lower()} = {class_name}( { params } )\n"
        code_string = f"return {class_name}( { params } )\n"

        return code_string

    def _generate_test_case(func_info: tuple) -> str:
        """Create a test case for a given function"""

        func_name = func_info[0]
        params = func_info[1]["params"]
        returns = func_info[1]["returns"]

        test_string = f"def test_{func_name}():\n\tassert True\n"
        return test_string

    def get_test_code(self):
        return self.test_code

    def report(self) -> None:
        print(self.test_code)


if __name__ == "__main__":

    code = """

class Queue:
    def __init__(self, size_max: int) -> None:
        assert size_max > 0
        self.max = size_max
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array("i", range(size_max))

    def empty(self) -> bool:
        return self.size != 0

    def full(self) -> bool:
        return self.size == self.max

    def enqueue(self, x: int) -> bool:
        if self.size == self.max:
            return False
        self.data[self.tail] = x
        self.size += 1
        self.tail += 1
        if self.tail == self.max:
            self.tail = 0
        return True

    def dequeue(self) -> Optional[int]:
        if self.size == 0:
            return None
        x = self.data[self.head]
        self.size -= 1
        self.head += 1
        if self.head == self.max:
            self.head = 0
        return x

class Queue2:
    def __init__(self, size_max: int) -> None:
        assert size_max > 0
        self.max = size_max
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array("i", range(size_max))

    def empty(self) -> bool:
        return self.size != 0

    def full(self) -> bool:
        return self.size == self.max

    def enqueue(self, x: int) -> bool:
        if self.size == self.max:
            return False
        self.data[self.tail] = x
        self.size += 1
        self.tail += 1
        if self.tail == self.max:
            self.tail = 0
        return True

    def dequeue(self) -> Optional[int]:
        if self.size == 0:
            return None
        x = self.data[self.head]
        self.size -= 1
        self.head += 1
        if self.head == self.max:
            self.head = 0
        return x


"""

    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    analyzer_out = analyzer.get_code_breakdown()

    tcg = TestCodeGenerator()

    for class_info in analyzer_out["classes"].items():
        tcg.test_code += TestCodeGenerator._generate_fixture_function(class_info)

    for func_info in analyzer_out["functions"].items():
        tcg.test_code += TestCodeGenerator._generate_test_case(func_info)

    tcg.report()
