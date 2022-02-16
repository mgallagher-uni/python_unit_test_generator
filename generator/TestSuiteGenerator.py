import os
import sys
import ast

from pprint import pprint

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from generator.FileGenerator import FileGenerator


class TestSuiteGenerator:

    def __init__(self, conf:dict, root_name: str):

        self.conf:dict = conf
        self.root_name: str = root_name
        self.root_obj = self.get_root_object(root_name)
        if self.root_obj == None:
            sys.exit(f"Could not find: {sys.path[-1]}\\{root_name}")

    def traverse_directory(self, ent: os.DirEntry) -> None:
        """Traverses through given directory creating corresponding test files in test directory."""

        print(f"Generator looking in: {ent.path[2:]}")

        directory = os.scandir(ent.path)
        for sub_ent in directory:
            
            # when a folder is found
            if sub_ent.is_dir():
                # do not enter ignored folders
                if sub_ent.name in self.conf["ignore_folders"]:
                    continue
                # enter folder and continue search
                else:
                    self.traverse_directory(sub_ent)

            # when a python file is found
            elif sub_ent.name.endswith(".py"):
                # do not generate for ignored files
                if sub_ent.name in self.conf["ignore_files"]:
                    continue
                # ignore other test files by default
                elif sub_ent.name.startswith("test_") or sub_ent.name.endswith("_test.py"):
                    continue
                # generate a test file for the given file
                else:
                    self.generate_file(sub_ent)

        directory.close()

    def generate_file(self, file_obj):
        tfg = FileGenerator(self.conf, self.root_name, file_obj.path)
        tfg.generate_file()

    def get_root_object(self, root_name: str):
        """Given the name of the directory find the DirEntry or FileEntry object"""
        temp_ents = os.scandir()
        for te in temp_ents:
            if te.name == root_name:
                temp_ents.close()
                return te

    def generate_suite(self) -> None:

        if self.root_obj.is_dir():
            self.traverse_directory(self.root_obj)

        if self.root_obj.is_file():
            self.generate_file(self.root_obj)

        with open( "conftest.py", "w+" ) as f:
            f.write("")

