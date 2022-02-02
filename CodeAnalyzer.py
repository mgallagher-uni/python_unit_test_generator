import ast
from pprint import pprint
from ast2json import ast2json


class CodeAnalyzer(ast.NodeVisitor):
    """
    An ast NodeVisitor which builds a dictionary representation of a tree
    """

    def __init__(self):
        self.code_breakdown = {"classes": {}, "functions": {}}
        self.class_linenos = []

    def visit_ClassDef(self, node) -> None:

        self.class_linenos += list(range(node.lineno, node.end_lineno))

        methods = node.body  # is body always a list of functions?
        # find __init__ function
        init = list(filter(CodeAnalyzer._is_init, methods))[0]
        # get init parameters and types
        params = CodeAnalyzer._get_params_from_FunctionDef(init)
        # add class info to code breakdown dictionary

        class_dict = {
            "params": params,
            "methods": {}
        }

        for method in node.body:

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


        self.code_breakdown["classes"][node.name] = class_dict
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
            self.code_breakdown["functions"][node.name] = func_dict
            self.generic_visit(node)


    def _is_init(node: ast.FunctionDef) -> bool:
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
