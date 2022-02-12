import pytest
import json

from generator.FileGenerator import FileGenerator

@pytest.fixture
def conf():
    with open("tests\\conf.json","r") as json_file:
        conf = json.load( json_file )
    return conf

def test__get_out_path(conf):
	fg = FileGenerator(conf, "mock_src", ".\\mock_src\\lib\\queue.py" )
	assert fg.testpath ==	".\\test_mock_src\\lib\\test_queue.py"

def test_generate_file():
	assert True

