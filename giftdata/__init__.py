from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from giftdata import download, urls
from utils import gift_xml_utils, path_utils
from views import dialog

gift_entity_list = {}
overall_gift_entity = None
progress_dialog = None
progress_value = 0


def init_gift_data(edit_gift):
    global progress_dialog
    progress_dialog = dialog.ProgressDialog(edit_gift)
    progress_dialog.setWindowTitle("为便捷而生")
    progress_dialog.setWindowIcon(QIcon('../favicon.ico'))
    # 下载数据
    download.load_config()
    analysis_gift_data()


def analysis_gift_data():
    # 下载数据成功后解析数据
    if download.get_gift_data_update_time():
        # 总表数据
        global overall_gift_entity
        overall_gift_entity = gift_xml_utils.analysis_overall_gift_xml(
            path_utils.get_download_path() + urls.OVERALL_XML_NAME)
        if overall_gift_entity:
            print("OverallGiftItem Count = %d" % len(overall_gift_entity.item_list))
        # 各项目数据
        gift_entity_list.clear()
        for path in urls.XML_NAME_LIST:
            gift_entity = gift_xml_utils.analysis_gift_xml(path_utils.get_download_path() + path)
            if gift_entity:
                gift_entity_list[path] = gift_entity
        print("GiftEntity Count = %d" % len(gift_entity_list))
        if not download.get_gift_icon_update_time():
            download.load_icon()
