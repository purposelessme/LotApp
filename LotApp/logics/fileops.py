from pathlib import Path


class FileOps:

    @staticmethod
    def list_files():
        files_list = list(Path("databases").glob("*.txt"))
        for index,file in enumerate(files_list):
            files_list[index] = file.name[0:-4]
        return files_list
