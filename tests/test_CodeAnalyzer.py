import pytest

@pytest.fixture
def temp_to_do():
	return CodeAnalyzer( [] )

def test_codeanalyzer_visit_ClassDef():
	assert True

def test_codeanalyzer_visit_FunctionDef():
	assert True

def test_codeanalyzer__is_init():
	assert True

def test_codeanalyzer__is_function():
	assert True

def test_codeanalyzer__get_params_from_FunctionDef():
	assert True

def test_codeanalyzer_get_code_dict():
	assert True

def test_codeanalyzer_report():
	assert True

