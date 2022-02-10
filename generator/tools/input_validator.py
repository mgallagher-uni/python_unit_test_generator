
from typing import Optional

def input_with_validation( message:str, t: type, specific:Optional[list]=None):
    
    while True:
        try:
            value = t(input(message + ": " ))

            if specific:
                if value not in specific:
                    spec_str = ", ".join(specific)
                    print(f"Input must be one of: { spec_str } ")
                    continue
            return value
        except:
            print(f"Input must be of type { t.__name__ }.")

if __name__ == "__main__":

    v = get_valid_input("Enter a number", int)
    print(v)



