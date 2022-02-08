import pytest

@pytest.fixture
def temp_to_do():
	return FileGenerator( [('root_dir', 'str'), ('filepath', 'str')] )

def test_filegenerator__get_out_path():
	assert True

def test_filegenerator_generate_file():
	assert True

