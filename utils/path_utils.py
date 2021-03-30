import getpass
import os


def get_cache_path():
    path = 'C:\\Users\\' + getpass.getuser() + '\\Kevin\\IjsGiftWall\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_download_path():
    path = 'C:\\Users\\' + getpass.getuser() + '\\Kevin\\IjsGiftWall\\download\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_database_path():
    path = 'C:\\Users\\' + getpass.getuser() + '\\Kevin\\IjsGiftWall\\database\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path
