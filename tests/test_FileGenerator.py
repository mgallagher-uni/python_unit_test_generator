import pytest

@pytest.fixture
def temp_to_do():
	return FileGenerator( 'root_dir', 'filepath' )

def test__get_out_path():
	assert True

def test_generate_file():
	assert True

