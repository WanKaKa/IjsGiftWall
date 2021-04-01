import os

from utils import path_utils
import json

normal_json_name = "normal_json_name.json"

KEY_GIFT_DATA_UPDATE_TIME = "key_gift_data_update_time"
KEY_GIFT_ICON_UPDATE_TIME = "key_gift_icon_update_time"


def get():
    path = path_utils.get_database_path() + normal_json_name
    if not os.path.exists(path):
        return None
    file = open(path, mode='r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()
    return data


def save(key, value):
    temp_data = get()
    temp_data = temp_data if temp_data else {}
    temp_data[key] = value
    file = open(path_utils.get_database_path() + normal_json_name, mode='w', encoding='utf-8')
    json.dump(temp_data, file, ensure_ascii=False)
    file.close()
