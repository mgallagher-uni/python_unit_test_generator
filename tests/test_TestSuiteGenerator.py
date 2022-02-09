import pytest
from generator.TestSuiteGenerator import TestSuiteGenerator

@pytest.fixture
def generator():
	return TestSuiteGenerator('prop_src')

@pytest.fixture
def prop_src():
	pass

def test_traverse_directory():
	assert True

def test_generation_with_nonexistant_root_dir():
	with pytest.raises(SystemExit):
		no_root_gen = TestSuiteGenerator('non_existant')

def test_generate_suite():
	assert True

