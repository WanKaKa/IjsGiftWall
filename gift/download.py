import os
import time

from database import json_
from gift import urls, entity, downloader
from util import xml_, path_

# 每个地区对应的表数据
gift_entity_list = {}
for language in urls.LANGUAGE_LIST:
    gift_entity_list[language] = {}
# 总表数据
overall_gift_entity = entity.OverallGiftEntity()


# 初始化数据
def init_gift_data(view_):
    DownloadConfig(view_)


# 下载数据成功后解析数据
def analysis_gift_data():
    if is_downloaded_config():
        # 总表数据
        global overall_gift_entity
        overall_gift_entity = xml_.analysis_overall_gift_xml(
            path_.get_download() + urls.OVERALL_XML_NAME)
        if overall_gift_entity:
            print("OverallGiftItem Count = %d" % len(overall_gift_entity.item_list))
        # 各地区表数据
        for i in range(len(gift_entity_list)):
            gift_entity_list[urls.LANGUAGE_LIST[i]].clear()
            language_ = urls.LANGUAGE_LIST[i]
            language_ = language_ + '\\' if language_ != urls.LANGUAGE_LIST[0] else ""
            for path in urls.XML_NAME_LIST:
                gift_entity = xml_.analysis_gift_xml(path_.get_download() + language_ + path)
                if gift_entity:
                    gift_entity_list[urls.LANGUAGE_LIST[i]][path] = gift_entity
            language_ = urls.LANGUAGE_LIST[i]
            print("地区 = %s 表数量 = %d" % (language_.ljust(20, " "), len(gift_entity_list[language_])))


class DownloadConfig:

    def __init__(self, view_):
        self.view_ = view_
        self.view_.download_start_time = time.time()
        if is_downloaded_config():
            analysis_gift_data()
            DownloadIcon(self.view_)
            return

        self.view_.show_progress_dialog(title="为便捷而生", message="正在下载配置文件，请稍等...")
        # 解析需要下载的配置列表
        file_path_list = [urls.OVERALL_XML_NAME]
        for language_ in urls.LANGUAGE_LIST:
            language_ = language_ + '/' if language_ != urls.LANGUAGE_LIST[0] else ""
            if not os.path.exists(path_.get_download() + language_):
                os.makedirs(path_.get_download() + language_)
            for name in urls.XML_NAME_LIST:
                file_path_list.append(language_ + name)
        # 开始下载
        downloader_ = downloader.Downloader(urls.BASE_URL, file_path_list, download_type="config")
        downloader_.my_signal.connect(self.view_.progress_callback)
        downloader_.run()


class DownloadIcon:

    def __init__(self, view_):
        self.view_ = view_
        if is_downloaded_icon() or not overall_gift_entity or not overall_gift_entity.item_list:
            self.view_.hide_progress_dialog()
            return

        self.view_.show_progress_dialog(title="为便捷而生", message="正在下载图片资源，请稍等...")
        # 解析需要下载的图标列表
        file_path_list = []
        for item in overall_gift_entity.item_list:
            if item.icon_image_path:
                dir_path = os.path.dirname(path_.get_download() + item.icon_image_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                file_path_list.append(item.icon_image_path)
            if item.poster_path:
                dir_path = os.path.dirname(path_.get_download() + item.poster_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                file_path_list.append(item.poster_path)
        # 开始下载
        downloader_ = downloader.Downloader(urls.BASE_URL, file_path_list, download_type="icon")
        downloader_.my_signal.connect(self.view_.progress_callback)
        downloader_.run()


def is_downloaded_config():
    return json_.get_config_download_time() > 0


def is_downloaded_icon():
    return json_.get_icon_download_time() > 0
