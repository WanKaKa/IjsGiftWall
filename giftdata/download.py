import os
import time

import requests
from utils import path_utils
import giftdata
from giftdata import urls
from database import database_json
from multiprocessing.pool import ThreadPool


class Downloader:

    def __init__(self, server_url, file_path_list, downloaded_callback):
        self.server_url = server_url
        self.file_path_list = file_path_list
        self.downloaded_callback = downloaded_callback
        self.downloaded_count = 0

    def down(self, file_path):
        file_url = self.server_url + file_path
        # print("下载文件网址 = " + file_url)
        r = requests.get(file_url)
        with open(path_utils.get_download_path() + file_path, "wb+") as fp:
            fp.write(r.content)
            giftdata.progress_value = giftdata.progress_value + 100 / len(self.file_path_list)
            giftdata.progress_dialog.progressBar.setProperty("value", giftdata.progress_value)
            self.downloaded_count = self.downloaded_count + 1
            if self.downloaded_count == len(self.file_path_list):
                self.downloaded_callback()

    def run(self):
        self.downloaded_count = 0
        ThreadPool(10).imap_unordered(self.down, self.file_path_list)


def start_config():
    giftdata.progress_value = 0
    giftdata.progress_dialog.label.setText("正在下载配置文件，请稍等...")
    giftdata.progress_dialog.show()
    file_path_list = [urls.OVERALL_XML_NAME]
    for name in urls.XML_NAME_LIST:
        file_path_list.append(name)
    download = Downloader(urls.BASE_URL, file_path_list, end_config)
    download.run()


def end_config():
    giftdata.progress_dialog.hide()
    database_json.save(database_json.KEY_GIFT_DATA_UPDATE_TIME,
                       {database_json.KEY_GIFT_DATA_UPDATE_TIME: time.time()})
    giftdata.analysis_gift_data()


def load_config():
    if get_gift_data_update_time():
        return
    start_config()


def reload_config():
    start_config()


def start_icon():
    giftdata.progress_value = 0
    giftdata.progress_dialog.label.setText("正在下载图片资源，请稍等...")
    giftdata.progress_dialog.show()
    if giftdata.overall_gift_entity:
        file_path_list = []
        for item in giftdata.overall_gift_entity.item_list:
            if item.icon_image_path:
                file_path_list.append(item.icon_image_path)
            if item.poster_path:
                file_path_list.append(item.poster_path)
        if not os.path.exists(path_utils.get_download_path() + 'icons'):
            os.makedirs(path_utils.get_download_path() + 'icons')
        if not os.path.exists(path_utils.get_download_path() + 'posters'):
            os.makedirs(path_utils.get_download_path() + 'posters')
        download = Downloader(urls.BASE_URL, file_path_list, end_icon)
        download.run()


def end_icon():
    giftdata.progress_dialog.hide()
    database_json.save(database_json.KEY_GIFT_ICON_UPDATE_TIME,
                       {database_json.KEY_GIFT_ICON_UPDATE_TIME: time.time()})


def load_icon():
    if get_gift_icon_update_time():
        return
    start_icon()


def reload_icon():
    start_icon()


def get_gift_data_update_time():
    json_data = database_json.get(database_json.KEY_GIFT_DATA_UPDATE_TIME)
    if json_data and database_json.KEY_GIFT_DATA_UPDATE_TIME in json_data:
        return float(json_data[database_json.KEY_GIFT_DATA_UPDATE_TIME])
    return None


def get_gift_icon_update_time():
    json_data = database_json.get(database_json.KEY_GIFT_ICON_UPDATE_TIME)
    if json_data and database_json.KEY_GIFT_ICON_UPDATE_TIME in json_data:
        return float(json_data[database_json.KEY_GIFT_ICON_UPDATE_TIME])
    return None
