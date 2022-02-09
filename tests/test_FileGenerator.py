import pytest

from generator.FileGenerator import FileGenerator

def test__get_out_path():
	fg = FileGenerator( "mock_src", ".\\mock_src\\lib\\queue.py" )
	assert fg.testpath ==	".\\test_mock_src\\lib\\test_queue.py"

def test_generate_file():
	assert True

