import os
import shutil


def delete_dir(dir_path):
    del_list = os.listdir(dir_path)
    for f in del_list:
        file_path = os.path.join(dir_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
