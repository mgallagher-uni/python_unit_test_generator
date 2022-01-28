import ast
from pprint import pprint


class CodeAnalyzer(ast.NodeVisitor):
    """
    An ast NodeVisitor which builds a dictionary representation of a tree
    """

    def __init__(self):
        self.code_breakdown = {"classes": {}, "functions": {}}

    def visit_ClassDef(self, node) -> None:

        methods = node.body  # is body always a list of functions?
        # find __init__ function
        init = list(filter(CodeAnalyzer._find_init, methods))[0]
        # get init parameters and types
        params = CodeAnalyzer._get_params_from_FunctionDef(init)
        # add class info to code breakdown dictionary
        class_dict = {
            "params": params,
            "methods": [func.name for func in methods].remove('__init__'),
        }
        self.code_breakdown["classes"][node.name] = class_dict
        self.generic_visit(node)


    def visit_FunctionDef(self, node) -> None:

        if node.name == "__init__":
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
            self.code_breakdown["functions"][node.name] = func_dict
            self.generic_visit(node)


    def _find_init(node: ast.FunctionDef) -> bool:
        return node.name == "__init__"

    def _get_params_from_FunctionDef(node: ast.FunctionDef()) -> list:
        params = [
            (arg.arg, arg.annotation.id if arg.annotation != None else "")
            for arg in node.args.args
        ]
        params.remove(("self", ""))
        return params

    def get_code_breakdown(self) -> dict:
        return self.code_breakdown

    def report(self) -> None:
        pprint(self.code_breakdown)
