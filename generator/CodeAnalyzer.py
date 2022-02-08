import ast
from pprint import pprint


class CodeAnalyzer(ast.NodeVisitor):
    """
    An ast NodeVisitor which builds a dictionary representation of a tree
    """

    def __init__(self):
        self.code_dict = {"classes": {}, "functions": {}}
        self.class_linenos = []

    def visit_ClassDef(self, node) -> None:

        self.class_linenos += list(range(node.lineno, node.end_lineno))

        methods = node.body
        methods = list(filter(CodeAnalyzer._is_function, methods))

        # does class inherit from base class/es
        bases = [
            base.id
            if isinstance(base, ast.Name)
            else base.value.id + "." + base.attr
            for base in node.bases
        ]

        # does class have an __init__ function
        # find __init__ function
        init = list(filter(CodeAnalyzer._is_init, methods))
        if init:
            # get init parameters and types
            params = CodeAnalyzer._get_params_from_FunctionDef(init[0])
        else:
            params = []

        # add class info to code breakdown dictionary

        class_dict = {"bases": bases, "params": params, "methods": {}}

        for method in methods:

            if method.name == "__init__":
                continue
            else:
                params = CodeAnalyzer._get_params_from_FunctionDef(method)

                # get return type
                returns = None
                if type(method.returns) is ast.Name:
                    returns = method.returns.id
                elif type(method.returns) is ast.Subscript:
                    returns = method.returns.slice.id  # can add optional info if needed

                # add function info to code breakdown dictionary
                func_dict = {"params": params, "returns": returns}

            class_dict["methods"][method.name] = func_dict

        self.code_dict["classes"][node.name] = class_dict
        self.generic_visit(node)

    def visit_FunctionDef(self, node) -> None:

        if node.lineno in self.class_linenos:
            self.generic_visit(node)

        elif node.name == "__init__":
            self.generic_visit(node)
        else:
            params = CodeAnalyzer._get_params_from_FunctionDef(node)

            # get return type
            returns = None
            if type(node.returns) is ast.Name:
                returns = node.returns.id
            elif type(node.returns) is ast.Subscript:
                returns = node.returns.slice.id  # can add optional info if needed

            # add function info to code breakdown dictionary
            func_dict = {"params": params, "returns": returns}
            self.code_dict["functions"][node.name] = func_dict
            self.generic_visit(node)

    def _is_init(node: ast.FunctionDef) -> bool:
        return node.name == "__init__"

    def _is_function(node: ast.AST) -> bool:
        return isinstance(node, ast.FunctionDef)

    def _get_params_from_FunctionDef(node: ast.FunctionDef()) -> list:
        # params = [
        #     (arg.arg, arg.annotation.id)
        #     if isinstance(arg.annotation, ast.Name)
        #     else (arg.arg, arg.annotation.value.id + "." + arg.annotation.attr)
        #     for arg in node.args.args
        # ]

        params = []

        for arg in node.args.args:
            if isinstance(arg.annotation, ast.Name):
                params.append((arg.arg, arg.annotation.id))
            elif isinstance(arg.annotation, ast.Attribute):
                params.append((arg.arg, arg.annotation.value.id + "." + arg.annotation.attr))
            else:
                params.append((arg.arg, ""))


        if ("self", "") in params:
            params.remove(("self", ""))
        return params

    def get_code_dict(self) -> dict:
        return self.code_dict

    def report(self) -> None:
        pprint(self.code_dict)


if __name__ == "__main__":
    code = """
import array
from typing import Optional


class Queue(ast.NodeVisitor):
    def __init__(self, size_max: int) -> None:
        assert size_max > 0
        self.max = size_max
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array("i", range(size_max))

    def set_size_max(self, max: int):
        self.max = max

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
    print(ast.dump(tree, indent=4))
