import os
import sys
import ast
from pprint import pprint

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from generator.FileGenerator import FileGenerator


class TestSuiteGenerator:
    def __init__(self, dir_name: str):

        self.root_name: str = dir_name
        self.root_obj: os.DirEntry = self.get_dir_object(dir_name)
        if self.root_obj == None:
            sys.exit(f"Could not find folder: {sys.path[-1]}\\{dir_name}")

    def traverse_directory(self, ent: os.DirEntry) -> None:
        """Traverses through given directory creating corresponding test files in test directory."""

        directory = os.scandir(ent.path)
        for sub_ent in directory:
            if sub_ent.is_dir():
                self.traverse_directory(sub_ent)

            elif sub_ent.name.endswith(".py"):
                tfg = FileGenerator(self.root_name, sub_ent.path)
                tfg.generate_file()

        directory.close()

    def get_dir_object(self, dir_name: str) -> os.DirEntry:
        """Given the name of the directory find the os.DirEntry object"""
        temp_ents = os.scandir()
        for te in temp_ents:
            if te.name == dir_name:
                temp_ents.close()
                return te

    def generate_suite(self) -> None:
        self.traverse_directory(self.root_obj)
