import sys
from TestSuiteGenerator import TestSuiteGenerator

try:
    root_dir = sys.argv[1]
except:
    print("No directory given")
    exit(1)

gen = TestSuiteGenerator(root_dir)
gen.generate_suite()
