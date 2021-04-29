import os
import json

import utils.path_

normal_json_name = "normal_json_name.json"

KEY_CONFIG_TIME = "key_config_time"
KEY_ICON_TIME = "key_icon_time"


def get():
    path = utils.path_.get_database() + normal_json_name
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
    file = open(utils.path_.get_database() + normal_json_name, mode='w', encoding='utf-8')
    json.dump(temp_data, file, indent=4, ensure_ascii=False)
    file.close()
