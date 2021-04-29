import os
import time

import database.json_
import gift.urls
import gift.entity
import gift.downloader
import utils.xml_
import utils.path_

# 每个地区对应的表数据
gift_entity_list = {}
for language in gift.urls.LANGUAGE_LIST:
    gift_entity_list[language] = {}
# 总表数据
overall_gift_entity = gift.entity.OverallGiftEntity()


def init_gift_data(view_):
    # 下载数据
    DownloadConfig(view_)


def analysis_gift_data():
    # 下载数据成功后解析数据
    if is_downloaded_gift_data():
        # 总表数据
        global overall_gift_entity
        overall_gift_entity = utils.xml_.analysis_overall_gift_xml(
            utils.path_.get_download() + gift.urls.OVERALL_XML_NAME)
        if overall_gift_entity:
            print("OverallGiftItem Count = %d" % len(overall_gift_entity.item_list))
        # 各地区表数据
        for i in range(len(gift_entity_list)):
            gift_entity_list[gift.urls.LANGUAGE_LIST[i]].clear()
            language_ = gift.urls.LANGUAGE_LIST[i]
            language_ = language_ + '\\' if language_ != gift.urls.LANGUAGE_LIST[0] else ""
            for path in gift.urls.XML_NAME_LIST:
                gift_entity = utils.xml_.analysis_gift_xml(utils.path_.get_download() + language_ + path)
                if gift_entity:
                    gift_entity_list[gift.urls.LANGUAGE_LIST[i]][path] = gift_entity
            print("地区 = %s GiftEntity Count = %d" % (
                gift.urls.LANGUAGE_LIST[i].ljust(20, " "), len(gift_entity_list[gift.urls.LANGUAGE_LIST[i]])))


class DownloadConfig:

    def __init__(self, view_):
        self.view_ = view_
        self.view_.download_start_time = time.time()
        if is_downloaded_gift_data():
            analysis_gift_data()
            DownloadIcon(self.view_)
            return

        self.view_.show_progress_dialog(title="为便捷而生", message="正在下载配置文件，请稍等...")
        file_path_list = [gift.urls.OVERALL_XML_NAME]
        for language_ in gift.urls.LANGUAGE_LIST:
            language_ = language_ + '/' if language_ != gift.urls.LANGUAGE_LIST[0] else ""
            if not os.path.exists(utils.path_.get_download() + language_):
                os.makedirs(utils.path_.get_download() + language_)
            for name in gift.urls.XML_NAME_LIST:
                file_path_list.append(language_ + name)
        downloader_ = gift.downloader.Downloader(gift.urls.BASE_URL, file_path_list, download_type="config")
        downloader_.my_signal.connect(self.view_.progress_callback)
        downloader_.run()


class DownloadIcon:

    def __init__(self, view_):
        self.view_ = view_
        if is_downloaded_gift_icon() or not overall_gift_entity or not overall_gift_entity.item_list:
            self.view_.hide_progress_dialog()
            return

        self.view_.show_progress_dialog(title="为便捷而生", message="正在下载图片资源，请稍等...")
        if overall_gift_entity:
            file_path_list = []
            for item in overall_gift_entity.item_list:
                if item.icon_image_path:
                    file_path_list.append(item.icon_image_path)
                if item.poster_path:
                    file_path_list.append(item.poster_path)
            if not os.path.exists(utils.path_.get_download() + 'icons'):
                os.makedirs(utils.path_.get_download() + 'icons')
            if not os.path.exists(utils.path_.get_download() + 'posters'):
                os.makedirs(utils.path_.get_download() + 'posters')
            downloader_ = gift.downloader.Downloader(gift.urls.BASE_URL, file_path_list, download_type="icon")
            downloader_.my_signal.connect(self.view_.progress_callback)
            downloader_.run()


def is_downloaded_gift_data():
    json_data = database.json_.get()
    if json_data and database.json_.KEY_CONFIG_TIME in json_data:
        return json_data[database.json_.KEY_CONFIG_TIME] > 0
    return False


def is_downloaded_gift_icon():
    json_data = database.json_.get()
    if json_data and database.json_.KEY_ICON_TIME in json_data:
        return json_data[database.json_.KEY_ICON_TIME] > 0
    return False
