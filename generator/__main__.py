import sys
from TestSuiteGenerator import TestSuiteGenerator

try:
    root_dir = sys.argv[1]
except:
    sys.exit("No directory given.")

gen = TestSuiteGenerator(root_dir)
gen.generate_suite()
