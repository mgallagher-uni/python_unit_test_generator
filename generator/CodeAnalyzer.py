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
            base.id if isinstance(base, ast.Name) else base.value.id + "." + base.attr
            for base in node.bases
        ]

        # if the class is a custom exception we won't create test cases
        if "Exception" in bases:
            self.generic_visit(node)

        # does class have an __init__ function
        # find __init__ function
        init = list(filter(CodeAnalyzer._is_init, methods))
        if init:
            # get init parameters and types
            params = self.get_params_from_FunctionDef(init[0])
        else:
            params = []

        # add class info to code breakdown dictionary
        class_dict = {"bases": bases, "params": params, "methods": {}}

        for method in methods:

            # init info already added as class params
            if method.name == "__init__":
                continue
            else:
                params = self.get_params_from_FunctionDef(method)

                # get return type
                returns = None
                if type(method.returns) is ast.Name:
                    returns = method.returns.id
                elif type(method.returns) is ast.Subscript:
                    returns = method.returns.value.id  # can add optional info if needed

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
            params = self.get_params_from_FunctionDef(node)

            # get return type
            returns = None
            if type(node.returns) is ast.Name:
                returns = node.returns.id
            elif type(node.returns) is ast.Subscript:
                returns = node.returns.value.id  # can add optional info if needed

            # add function info to code breakdown dictionary
            func_dict = {"params": params, "returns": returns}
            self.code_dict["functions"][node.name] = func_dict
            self.generic_visit(node)

    def _is_init(node: ast.FunctionDef) -> bool:
        return node.name == "__init__"

    def _is_function(node: ast.AST) -> bool:
        return isinstance(node, ast.FunctionDef)

    def get_params_from_FunctionDef(self, node: ast.FunctionDef()) -> list:

        params = []

        for arg in node.args.args:
            if isinstance(arg.annotation, ast.Name):
                params.append((arg.arg, arg.annotation.id))
            elif isinstance(arg.annotation, ast.Attribute):
                params.append(
                    (arg.arg, arg.annotation.value.id + "." + arg.annotation.attr)
                )
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
class TimerError(Exception):
    def something():
        print("somethign")

@dataclass
class Timer(ContextDecorator):

    timers: ClassVar[Timers] = Timers()
    _start_time: Optional[float] = field(default=None, init=False, repr=False)
    name: Optional[str] = None
    text: Union[str, Callable[[float], str]] = "Elapsed time: {:0.4f} seconds"
    logger: Optional[Callable[[str], None]] = print
    last: float = field(default=math.nan, init=False, repr=False)

    def start(self) -> None:
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()
"""
    tree = ast.parse(code)
    ca = CodeAnalyzer()
    ca.visit(tree)
    pprint(ca.code_dict)
