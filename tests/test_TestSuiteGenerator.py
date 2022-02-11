import pytest
import os
import shutil
from generator.TestSuiteGenerator import TestSuiteGenerator


@pytest.fixture
def conf():
    return {
        "ignore_folders": ["__pycache__"],
        "ignore_files": ["__init__.py", "__main__.py"],
        "class_names_in_functions": False,
    }


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


def test_generator_with_nonexistant_root_dir():
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
