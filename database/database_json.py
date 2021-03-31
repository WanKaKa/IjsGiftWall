import os

from utils import path_utils
import json

KEY_GIFT_DATA_UPDATE_TIME = "key_gift_data_update_time"
KEY_GIFT_ICON_UPDATE_TIME = "key_gift_icon_update_time"


def get(file_name):
    path = path_utils.get_database_path() + file_name + ".json"
    if not os.path.exists(path):
        return
    file = open(path, mode='r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()
    return data


def save(file_name, data):
    file = open(path_utils.get_database_path() + file_name + ".json", mode='w', encoding='utf-8')
    json.dump(data, file, ensure_ascii=False)
    file.close()
