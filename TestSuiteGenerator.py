import os
import sys
import ast
from pprint import pprint

from FileGenerator import FileGenerator


class TestSuiteGenerator:
    def __init__(self, root_dir: str):

        self.root_dir = root_dir
        self.filepath: str
        self.testpath: str


    def traverse_directory(self, ent: os.DirEntry) -> None:
        """Traverses through given directory creating corresponding test files in test directory."""

        directory = os.scandir(ent.path)
        for sub_ent in directory:
            if sub_ent.is_dir():
                self.traverse_directory(sub_ent)

            elif sub_ent.name.endswith(".py"):

                tfg = FileGenerator(self.root_dir, sub_ent.path)
                tfg.generate_file()

        directory.close()

    def _get_dir_object( dir_name: str ) -> os.DirEntry:
        """Given the name of the directory find the os.DirEntry object"""
        temp_ents = os.scandir()
        for te in temp_ents:
            if te.name == dir_name:
                temp_ents.close()
                return te    

    def generate_suite(self) -> None:

        dir_object = TestSuiteGenerator._get_dir_object(self.root_dir)
        self.traverse_directory(dir_object)




if __name__ == "__main__":

    try:
        root_dir = sys.argv[1]
    except:
        print("No directory given")
        exit(0)

    gen = TestSuiteGenerator(root_dir)
    gen.generate_suite()
