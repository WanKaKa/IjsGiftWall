import os

from utils import path_utils
import json

json_ijs_normal = "ijs_normal.json"

KEY_GIFT_DATA_UPDATE_TIME = "key_gift_data_update_time"


def get():
    path = path_utils.get_database_path() + json_ijs_normal
    if not os.path.exists(path):
        return
    file = open(path_utils.get_database_path() + json_ijs_normal, mode='r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()
    return data


def save(data):
    file = open(path_utils.get_database_path() + json_ijs_normal, mode='w', encoding='utf-8')
    json.dump(data, file, ensure_ascii=False)
    file.close()
