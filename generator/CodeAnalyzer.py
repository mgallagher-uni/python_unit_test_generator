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
        methods = list(filter( lambda node: isinstance(node, ast.FunctionDef), methods))

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
        init = list(filter( lambda node: node.name == "__init__", methods))
        if init:
            # get init parameters and types
            params = self.get_params_from_FunctionDef(init[0])
        else:
            params = []

        # add class info to code breakdown dictionary
        class_dict = {"bases": bases, "params": params, "methods": {}, "setters": {}, "getters":{}}

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

            if CodeAnalyzer._is_setter(method):
                class_dict["setters"][method.name] = func_dict

            elif CodeAnalyzer._is_getter(method):
                class_dict["getters"][method.name] = func_dict
            else:
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

    def _is_setter(node: ast.FunctionDef) -> bool:
        """Checks for several attributes of a setter function"""

        try:
            if not node.name.startswith("set_"):
                return False
            elif not "self" in [ arg.arg for arg in node.args.args ]:
                return False
            elif not len(node.body) == 1 and type(node.body[0]) is ast.Assign:
                return False
            elif not node.body[0].targets[0].value.id == "self":
                return False
            return True
        except AttributeError:
            # print(ast.dump(node, indent=4))
            # print()


            # print(node.name)
            # print(node.name.startswith("set_"))
            # print("self" in [ arg.arg for arg in node.args.args ])
            # print(len(node.body) == 1)
            # # print(node.body[0].targets.value.id == "self")
            # # print()


            return False

    def _is_getter(node: ast.FunctionDef) -> bool:
        """Checks for several attributes of a getter function"""
        try:
            if not node.name.startswith("get_"):
                print(1)
                return False
            elif not node.args.args[0].arg == "self":
                print(2)
                return False
            elif not len(node.body) == 1 and type(node.body[0]) is ast.Return:
                print(3)
                return False
            elif not node.body[0].value.value.id == "self":
                print(4)
                return False
            return True
        except AttributeError:
            print()
            return False

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
class RockPaperScissors:

    user_input = InputConsole()
    user_output = OutputConsole()
    computer_input = InputRandom()
    config = None
    property = None

    def __init__(self, config=ConfigFromFile()):
        self.config = config
        self.property = config.get_config()

    def set_user_input(self, user_input):
        self.user_input = user_input

    def set_computer_input(self, computer_input):
        self.computer_input = computer_input

    def set_user_output (self, user_output):
        self.user_output = user_output

    def set_config(self, config):
        self.config = config
        self.property = config.get_config()

    def determine_winner(self, player, computer):
        if player == computer:
            result = "Draw"
        elif (player + 1)%3 == computer:
            result = "Player wins"
        elif (computer + 1)%3 == player:
            result = "Computer Wins"
        return result

    def get_user_choice_request(self, weapons):
        request = "Select "
        for counter in range(len(weapons)):
            request += str(counter) + " for " + weapons[counter] + " "
        return request

    def get_user_choice(self, weapons):
        request = self.get_user_choice_request(weapons)
        player = self.user_input.get_input_int(request)
        if player in [0, 1, 2]:
            self.user_output.print("You selected " + weapons[player])
        return player

    def get_computer_choice(self, weapons):
        chosen = self.computer_input.get_input_int("")
        self.user_output.print("Computer chose " + weapons[chosen])
        return chosen

    def set_property(self):
        if self.property == []:
            self.property = self.config.get_config()

    def get_list_of_games(self):
        self.set_property()
        list_of_games = []
        for counter in range(1, len(self.property)):
            list_of_games.append(self.property[counter].split(":")[0])
        return list_of_games

    def get_weapon_lists(self):
        self.set_property()
        weapon_lists = []
        for counter in range(1, len(self.property)):
            weapon_lists.append(self.property[counter].split(":")[1].split(","))
        return weapon_lists

    def get_games_request(self, list_of_games):
        request = "Please select"
        for counter in range(len(list_of_games)):
            request += " " + str(counter) + " - " + list_of_games[counter]
        return request

    def generate_games_list_request(self):
        list_of_games = self.get_list_of_games()
        request = self.get_games_request(list_of_games)
        return request

    def get_game(self):
        request = self.generate_games_list_request()
        user_game = self.user_input.get_input_int(request)
        weapons_lists = self.get_weapon_lists()
        return weapons_lists[user_game]

    def play(self):
        weapon = self.get_game()
        player = self.get_user_choice(weapon)
        while player in [0, 1, 2]:
            computer = self.get_computer_choice(weapon)
            result = self.determine_winner(player, computer)
            self.user_output.print(result)
            player = self.get_user_choice(weapon)
"""
    tree = ast.parse(code)
    ca = CodeAnalyzer()
    ca.visit(tree)
    pprint(ca.code_dict)
