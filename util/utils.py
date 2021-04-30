import os
import shutil

from gift import urls
from util import path_


def delete_dir(dir_path):
    del_list = os.listdir(dir_path)
    for f in del_list:
        file_path = os.path.join(dir_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def get_outputs_dir_list():
    dir_list = [urls.LANGUAGE_LIST[0]]
    file_list = os.listdir(path_.get_outputs())
    for file_name in file_list:
        if os.path.isdir(path_.get_outputs() + file_name):
            dir_list.append(file_name)
    return dir_list


def compare_entity(entity1, entity2):
    title1 = entity1.title if entity1.title else ""
    package_name1 = entity1.package_name if entity1.package_name else ""
    title2 = entity2.title if entity2.title else ""
    package_name2 = entity2.package_name if entity2.package_name else ""
    return title1 == title2 and package_name1 == package_name2


def is_entity_added(entity_, entity_list):
    title1 = entity_.title if entity_.title else ""
    package_name1 = entity_.package_name if entity_.package_name else ""
    for value in entity_list:
        title2 = value.title if value.title else ""
        package_name2 = value.package_name if value.package_name else ""
        if title1 == title2 and package_name1 == package_name2:
            return True
    return False
