import pytest
import os
import shutil
import json
from generator.TestSuiteGenerator import TestSuiteGenerator


@pytest.fixture
def conf():
    with open("tests\\conf.json","r") as json_file:
        conf = json.load( json_file )
    return conf


@pytest.fixture
def generator(conf):
    return TestSuiteGenerator(conf, "mock_src")


@pytest.fixture
def mock_src_generated():
    with open("tests\\sample_code.txt", "r") as f:
        code = f.read()

    os.makedirs("mock_src\\lib\\no_py", exist_ok=True)
    os.makedirs("mock_src\\docs", exist_ok=True)

    with open("mock_src\\model.py", "w") as f:
        f.write(code)
    with open("mock_src\\lib\\queue.py", "w") as f:
        f.write(code)
    with open("mock_src\\docs\\not_py.txt", "w") as f:
        f.write("File is not a .py script")
    with open("mock_src\\lib\\no_py\\not_py.txt", "w") as f:
        f.write("File is not a .py script")


def test_generator_with_nonexistant_root_():
    with pytest.raises(SystemExit):
        no_root_gen = TestSuiteGenerator(conf, "non_existant")


def test_generate_suite(mock_src_generated, generator):

    generator.generate_suite()

    assert (
        os.path.isfile("test_mock_src\\test_model.py")
        and os.path.isfile("test_mock_src\\lib\\test_queue.py")
        and os.path.isfile("conftest.py")
    )

    # clean up
    shutil.rmtree("test_mock_src")
