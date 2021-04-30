import os
import json

from util import path_

# json数据文件名
normal_json_name = "normal_json_name.json"

# 配置表下载完成时间
KEY_CONFIG_DOWNLOAD_TIME = "key_config_download_time"
# 图片资源下载完成时间
KEY_ICON_DOWNLOAD_TIME = "key_icon_download_time"


def get_config_download_time():
    data = get()
    if data and KEY_CONFIG_DOWNLOAD_TIME in data:
        return data[KEY_CONFIG_DOWNLOAD_TIME]
    return 0


def put_config_download_time(value):
    save(KEY_CONFIG_DOWNLOAD_TIME, value)


def get_icon_download_time():
    data = get()
    if data and KEY_ICON_DOWNLOAD_TIME in data:
        return data[KEY_ICON_DOWNLOAD_TIME]
    return 0


def put_icon_download_time(value):
    save(KEY_ICON_DOWNLOAD_TIME, value)


def get():
    path = path_.get_database() + normal_json_name
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
    file = open(path_.get_database() + normal_json_name, mode='w', encoding='utf-8')
    json.dump(temp_data, file, indent=4, ensure_ascii=False)
    file.close()
