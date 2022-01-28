import ast
from pprint import pprint

def generate_class_init_fixture( class_name: str, params: list ):

    param_names, param_types = zip(*params)

    function_name = "new_" + class_name
    
    code_string = f"""@pytest.fixture\ndef {function_name}():\n\t{class_name.lower()} = {class_name}( { params } )"""

    return code_string
    


class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.code_breakdown = { "classes": [], "functions": [] }

    def visit_ClassDef(self, node) -> None:

        methods = node.body                                 # is body always a list of functions?

        # find __init__ function
        init = list(filter( CodeAnalyzer._find_init, methods ))[0]

        # get init parameters and types
        params = CodeAnalyzer._get_params_from_FunctionDef(init)

        # add class info to code breakdown dictionary
        class_dict = { node.name: { "init_params": params, "methods": [ func.name for func in methods ]}}
        self.code_breakdown["classes"].append( class_dict )

        self.generic_visit(node)
    

    def visit_FunctionDef(self, node) -> None:        

        params = CodeAnalyzer._get_params_from_FunctionDef(node)

        # get return type 
        return_type = None        
        if type(node.returns) is ast.Name:
            return_type = node.returns.id
        elif type(node.returns) is ast.Subscript:
            return_type = node.returns.slice.id           # can add optional info if needed

        # add function info to code breakdown dictionary
        func_dict = { node.name: { "params": params, "return": return_type } }
        self.code_breakdown["functions"].append( func_dict )

        self.generic_visit(node)


    def _find_init(node: ast.FunctionDef) -> bool:
        return node.name == "__init__"

    def _get_params_from_FunctionDef(node: ast.FunctionDef()) -> list:
        params = [ (arg.arg, arg.annotation.id if arg.annotation != None else "") for arg in node.args.args ]
        params.remove(('self', ''))
        return params

    def get_code_breaksown(self) -> dict :
        return self.code_breakdown

    def report(self) -> None:
        pprint(self.code_breakdown)


tree = ast.parse(code)
analyzer = CodeAnalyzer()
analyzer.visit(tree)
analyzer.report()
