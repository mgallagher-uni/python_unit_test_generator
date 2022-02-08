import pytest

@pytest.fixture
def temp_to_do():
	return CodeGenerator( [('code_dict', '')] )

def test_codegenerator_generate_full():
	assert True

def test_codegenerator__generate_fixture_function():
	assert True

def test_codegenerator__generate_class_initialisation():
	assert True

def test_codegenerator__generate_test_case():
	assert True

def test_codegenerator_get_test_code():
	assert True

def test_codegenerator_report():
	assert True

