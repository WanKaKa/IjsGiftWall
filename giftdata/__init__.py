import os
import time

from database import database_json
from giftdata import download, urls
from giftdata.download import Downloader
from utils import gift_xml_utils, path_utils, ico_utils
from views import dialog

gift_entity_list = {
    urls.LANGUAGE_LIST[0]: {},
    urls.LANGUAGE_LIST[1]: {},
    urls.LANGUAGE_LIST[2]: {},
    urls.LANGUAGE_LIST[3]: {},
    urls.LANGUAGE_LIST[4]: {},
    urls.LANGUAGE_LIST[5]: {},
    urls.LANGUAGE_LIST[6]: {},
    urls.LANGUAGE_LIST[7]: {},
    urls.LANGUAGE_LIST[8]: {},
    urls.LANGUAGE_LIST[9]: {},
    urls.LANGUAGE_LIST[10]: {},
}
overall_gift_entity = None


class LoadConfig:

    def __init__(self, edit_gift_view):
        self.edit_gift_view = edit_gift_view
        self.edit_gift_view.download_start_time = time.time()
        if get_gift_data_update_time():
            analysis_gift_data()
            LoadIcon(self.edit_gift_view)
            return
        self.edit_gift_view.progress_dialog = dialog.ProgressDialog(self.edit_gift_view)
        self.edit_gift_view.progress_dialog.setWindowTitle("为便捷而生")
        self.edit_gift_view.progress_dialog.setWindowIcon(ico_utils.get_logo_icon())
        self.edit_gift_view.progress_dialog.label.setText("正在下载配置文件，请稍等...")
        self.edit_gift_view.progress_dialog.progressBar.setProperty("value", 0)
        self.edit_gift_view.progress_dialog.show()
        file_path_list = [urls.OVERALL_XML_NAME]
        for language in urls.LANGUAGE_LIST:
            language = language + '/' if language != urls.LANGUAGE_LIST[0] else ""
            if not os.path.exists(path_utils.get_download_path() + language):
                os.makedirs(path_utils.get_download_path() + language)
            for name in urls.XML_NAME_LIST:
                file_path_list.append(language + name)
        downloader = Downloader(urls.BASE_URL, file_path_list, download_type="config")
        downloader.my_signal.connect(self.edit_gift_view.progress_callback)
        downloader.run()


class LoadIcon:

    def __init__(self, edit_gift_view, progress_dialog=None):
        self.edit_gift_view = edit_gift_view
        if get_gift_icon_update_time() or not overall_gift_entity or not overall_gift_entity.item_list:
            if progress_dialog:
                progress_dialog.hide()
            return
        if progress_dialog:
            self.edit_gift_view.progress_dialog = progress_dialog
        else:
            self.edit_gift_view.progress_dialog = dialog.ProgressDialog(self.edit_gift_view)
        self.edit_gift_view.progress_dialog.setWindowTitle("为便捷而生")
        self.edit_gift_view.progress_dialog.setWindowIcon(ico_utils.get_logo_icon())
        self.edit_gift_view.progress_dialog.label.setText("正在下载图片资源，请稍等...")
        self.edit_gift_view.progress_dialog.progressBar.setProperty("value", 0)
        self.edit_gift_view.progress_dialog.show()
        if overall_gift_entity:
            file_path_list = []
            for item in overall_gift_entity.item_list:
                if item.icon_image_path:
                    file_path_list.append(item.icon_image_path)
                if item.poster_path:
                    file_path_list.append(item.poster_path)
            if not os.path.exists(path_utils.get_download_path() + 'icons'):
                os.makedirs(path_utils.get_download_path() + 'icons')
            if not os.path.exists(path_utils.get_download_path() + 'posters'):
                os.makedirs(path_utils.get_download_path() + 'posters')
            downloader = Downloader(urls.BASE_URL, file_path_list, download_type="icon")
            downloader.my_signal.connect(self.edit_gift_view.progress_callback)
            downloader.run()


def init_gift_data(edit_gift_view):
    # 下载数据
    LoadConfig(edit_gift_view)


def analysis_gift_data():
    # 下载数据成功后解析数据
    if get_gift_data_update_time():
        # 总表数据
        global overall_gift_entity
        overall_gift_entity = gift_xml_utils.analysis_overall_gift_xml(
            path_utils.get_download_path() + urls.OVERALL_XML_NAME)
        if overall_gift_entity:
            print("OverallGiftItem Count = %d" % len(overall_gift_entity.item_list))
        # 各项目数据
        for i in range(len(gift_entity_list)):
            gift_entity_list[urls.LANGUAGE_LIST[i]].clear()
            language = urls.LANGUAGE_LIST[i] + '\\' if urls.LANGUAGE_LIST[i] != urls.LANGUAGE_LIST[0] else ""
            for path in urls.XML_NAME_LIST:
                gift_entity = gift_xml_utils.analysis_gift_xml(path_utils.get_download_path() + language + path)
                if gift_entity:
                    gift_entity_list[urls.LANGUAGE_LIST[i]][path] = gift_entity
            print("地区 = %s GiftEntity Count = %d" % (
                urls.LANGUAGE_LIST[i].ljust(20, " "), len(gift_entity_list[urls.LANGUAGE_LIST[i]])))


def get_gift_data_update_time():
    json_data = database_json.get()
    if json_data and database_json.KEY_GIFT_DATA_UPDATE_TIME in json_data:
        return float(json_data[database_json.KEY_GIFT_DATA_UPDATE_TIME])
    return None


def get_gift_icon_update_time():
    json_data = database_json.get()
    if json_data and database_json.KEY_GIFT_ICON_UPDATE_TIME in json_data:
        return float(json_data[database_json.KEY_GIFT_ICON_UPDATE_TIME])
    return None
