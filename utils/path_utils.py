import getpass
import os


def get_cache_path():
    path = 'C:\\IJoySoft\\' + 'Kevin\\IjsGiftWall\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_download_path():
    path = 'C:\\IJoySoft\\' + 'Kevin\\IjsGiftWall\\download\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_database_path():
    path = 'C:\\IJoySoft\\' + 'Kevin\\IjsGiftWall\\database\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_outputs_path():
    path = 'C:\\IJoySoft\\' + 'Kevin\\IjsGiftWall\\outputs\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path
