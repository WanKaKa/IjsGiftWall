import os

ROOT_PATH = 'C:\\IJoySoft\\Kevin\\IjsGiftWall\\'


def get_cache():
    path = ROOT_PATH
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_download():
    path = ROOT_PATH + 'download\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_database():
    path = ROOT_PATH + 'database\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_outputs():
    path = ROOT_PATH + 'outputs\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path
