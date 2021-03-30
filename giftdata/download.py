import threading
import time

import requests
from utils import path_utils
from giftdata import urls
from database import database_json


class Downloader:

    def __init__(self, server_url, file_path_list):
        self.server_url = server_url
        self.file_path_list = file_path_list

        self.thread_list = []
        for file_path in file_path_list:
            self.thread_list.append(threading.Thread(target=self.down, args=(file_path,)))

    def down(self, file_path):
        file_url = self.server_url + file_path
        # print("下载文件网址 = " + file_url)
        r = requests.get(file_url)
        with open(path_utils.get_download_path() + file_path, "wb+") as fp:
            fp.write(r.content)

    def run(self):
        for thread in self.thread_list:
            print("开始下载 = %s" % thread.getName())
            thread.start()
        for thread in self.thread_list:
            print("完成下载 = %s" % thread.getName())
            thread.join()
        print(str(time.time()))
        database_json.save({database_json.KEY_GIFT_DATA_UPDATE_TIME: time.time()})


def start():
    file_path_list = [urls.OVERALL_XML_NAME]
    for name in urls.XML_NAME_LIST:
        file_path_list.append(name)
    download = Downloader(urls.BASE_URL, file_path_list)
    download.run()


def load():
    gift_data_update_time = get_update_time()
    if gift_data_update_time:
        time_interval = time.time() - gift_data_update_time
        if time_interval <= 3600 * 24 * 2:
            print("GiftWall自动更新 : 时间隔间=48H, 现在 : 间隔时间=%.2fH" % (time_interval / 3600))
            return
    start()


def reload():
    start()


def get_update_time():
    json_data = database_json.get()
    if json_data and database_json.KEY_GIFT_DATA_UPDATE_TIME in json_data:
        return float(json_data[database_json.KEY_GIFT_DATA_UPDATE_TIME])
