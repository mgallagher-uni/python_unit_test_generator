import os
import sys
import ast


class FileStructureGenerator:
    def __init__(self):
        self.prefix = "test_"

        if len(sys.argv) == 1:
            print("No directory given")
            exit(0)
        else:
            self.root_dir = str(sys.argv[1])
        
        self.traverse_directory(self.get_dir_object(self.root_dir))

    def get_dir_object(self, dir_name: str) -> os.DirEntry:
        '''Given the name of the directory find the os.DirEntry object'''
        temp_ents = os.scandir()
        for te in temp_ents:
            if te.name == dir_name:
                temp_ents.close()
                return te

    def create_test_file(self, ent: os.DirEntry) -> None:
        '''Create a test file for a python module in the corresponding folder in the test directory.'''

        test_route = os.path.split(ent.path)[0].replace( self.root_dir, self.prefix + self.root_dir )
        test_path = ent.path.replace(ent.name, self.prefix + ent.name ).replace(  self.root_dir, self.prefix + self.root_dir )

        # if route does not exist create it
        os.makedirs(test_route, exist_ok=True)

        # if file does not already exist
        if not os.path.exists(test_path):
            # create the test file in the corresponding location
            test_file = open( test_path, 'w')
            test_file.write("print(\"Hello test file!\")")
            test_file.close()
    
    def traverse_directory(self, ent: os.DirEntry) -> None:
        directory = os.scandir(ent.path)
        for sub_ent in directory:
            if sub_ent.is_dir():
                self.traverse_directory(sub_ent)
            elif sub_ent.name.endswith(".py"):
                self.create_test_file(sub_ent)
        directory.close()


if __name__ == "__main__":
    FileStructureGenerator()