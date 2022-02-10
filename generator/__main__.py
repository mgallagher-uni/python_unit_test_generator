import sys
import json
import shutil

from tools.input_validator import *
from TestSuiteGenerator import TestSuiteGenerator

try:
    root_dir = sys.argv[1]
except:
    sys.exit("No directory given.")

with open("generator\\conf.json", "r") as j:
    conf = json.load(j)

# have user configure some settings
response = input_with_validation("Configure settings? (y/n)", str, ["y", "n"])

if response == "y":
    cnif = input_with_validation("Class names in functions? (y/n)", str, ["y", "n"])
    conf["class_names_in_functions"] = True if cnif == "y" else False


gen = TestSuiteGenerator(conf, root_dir)
gen.generate_suite()

# clean up
with open("generator\\conf.json", "w") as j:
    json.dump(conf, j)

shutil.rmtree("test_mock_src")

