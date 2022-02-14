import sys
import json
import shutil

from tools.input_prompt_types import *
from TestSuiteGenerator import TestSuiteGenerator

try:
    root_dir = sys.argv[1]
except:
    sys.exit("No directory given.")

with open("generator\\conf.json", "r") as j:
    conf = json.load(j)


#user configure some settings
if input_y_n("Configure settings?"):
    
    # Generate for setter/getters?
    conf["setters_getters"] = input_y_n("Generate tests for setter/getters?")

    # add folders to ignore list
    if input_y_n("Add to folder ignore list?"):
        folder_name = input("Enter folder name to be ignored: ")
        conf["ignore_folders"].append(folder_name)
    else:
        print("Ignore folders can be added directly to conf.json file.")
    
    # add files to ignore list
    if input_y_n("Add to files ignore list?"):
        file_name = input("Enter file name to be ignored: ")
        conf["ignore_files"].append(file_name)
    else:
        print("Ignore files can be added directly to conf.json file.")

    # use class names in functions?
    conf["class_names_in_functions"] = input_y_n("Class names in functions?")

    # save conf file
    with open("generator\\conf.json", "w") as json_file:
        json.dump(conf, json_file)

# display current settings
print(f"""
Settings

Test setters/getters: { conf["setters_getters"] }
Ignoring folders: { ", ".join(conf["ignore_folders"]) }
Ignoring files: { ", ".join(conf["ignore_files"]) }
Add class names to test functions: { conf["class_names_in_functions"] }

""")

# run the generator
gen = TestSuiteGenerator(conf, root_dir)
gen.generate_suite()
