from typing import Optional, Type


def input_with_validation(message: str, t: type = str, specific: Optional[list] = None):
    
    while True:
        try:
            value = t(input(message + ": "))

            if specific:
                if value not in specific:
                    spec_str = ", ".join(specific)
                    print(f"Input must be one of: { spec_str } ")
                    continue
            return value
        except:
            print(f"Input must be of type { t.__name__ }.")


def input_y_n(message: str) -> bool:

    t = str
    specific = ["Y", "y", "Yes", "yes", "N", "n", "No", "no"]
    inp = input_with_validation(message + " (y/n)", t, specific)
    inp = inp.lower()[0]

    return True if inp == "y" else False


if __name__ == "__main__":

    v = get_valid_input("Enter a number", int)
    print(v)
