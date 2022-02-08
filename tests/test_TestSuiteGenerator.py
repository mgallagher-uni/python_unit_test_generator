import pytest

import os, sys
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from generator.TestSuiteGenerator import TestSuiteGenerator


@pytest.fixture
def generator():
	return TestSuiteGenerator( 'root_dir' )

def test_testsuitegenerator_traverse_directory():
	assert True

def test_testsuitegenerator__get_dir_object(generator):


	incorrect_filename = "not_a_file"

	result = generator._get_dir_object( incorrect_filename )
	
	assert result is None

def test_testsuitegenerator__get_dir_object():
	assert True

def test_testsuitegenerator_generate_suite():
	assert True

