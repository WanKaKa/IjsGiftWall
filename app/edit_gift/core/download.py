import os
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

from database import json_pro
from app.edit_gift.core import entity, urls, downloader, xml_pro
from util import path_pro

# 每个地区对应的表数据
gift_entity_list = {}
for language in urls.LANGUAGE_LIST:
    gift_entity_list[language] = {}
# 总表数据
overall_gift_entity = entity.OverallGiftEntity()


class _DownloadBridge(QObject):
    """后台准备完成后切回 UI 线程启动下载。"""
    config_parsed = pyqtSignal(bool)  # force
    icon_list_ready = pyqtSignal(object, bool)  # file_path_list, force

    def __init__(self, view):
        super(_DownloadBridge, self).__init__(view)
        self.view = view
        self.config_parsed.connect(self._on_config_parsed)
        self.icon_list_ready.connect(self._on_icon_list_ready)

    def _on_config_parsed(self, force):
        DownloadIcon(self.view, force=force)

    def _on_icon_list_ready(self, file_path_list, force):
        view = self.view
        view.show_progress_dialog(
            title="为便捷而生",
            message="正在下载图片资源，请稍等",
            busy=False,
        )
        downloader_ = downloader.Downloader(
            urls.BASE_URL, file_path_list, download_type="icon", skip_existing=not force)
        downloader_.my_signal.connect(view.progress_callback)
        view._active_downloader = downloader_
        downloader_.run()


def _ensure_bridge(view_):
    bridge = getattr(view_, "_download_bridge", None)
    if bridge is None:
        bridge = _DownloadBridge(view_)
        view_._download_bridge = bridge
    return bridge


# 初始化服务器GiftWall数据
def init_gift_data(view_, force=False):
    # 解析需要下载的配置列表
    file_path_list = [urls.OVERALL_XML_NAME]
    for language_ in urls.LANGUAGE_LIST:
        language_ = language_ + '/' if language_ != urls.LANGUAGE_LIST[0] else ""
        if not os.path.exists(path_pro.get_download() + language_):
            os.makedirs(path_pro.get_download() + language_)
        for name in urls.XML_NAME_LIST:
            if not name:
                continue
            file_path_list.append(language_ + name)
    DownloadConfig(view_, file_path_list, force=force)


# 下载数据成功后解析数据
def analysis_gift_data():
    if is_downloaded_config():
        # 总表数据
        global overall_gift_entity
        overall_gift_entity = xml_pro.analysis_overall_gift_xml(
            path_pro.get_download() + urls.OVERALL_XML_NAME)
        if overall_gift_entity:
            print("总表 - 产品数量 = %d" % len(overall_gift_entity.item_list))
        # 各地区表数据
        for i in range(len(gift_entity_list)):
            gift_entity_list[urls.LANGUAGE_LIST[i]].clear()
            language_ = urls.LANGUAGE_LIST[i]
            language_ = language_ + '\\' if language_ != urls.LANGUAGE_LIST[0] else ""
            for path in urls.XML_NAME_LIST:
                if not path:
                    continue
                gift_entity = xml_pro.analysis_gift_xml(path_pro.get_download() + language_ + path)
                if gift_entity:
                    gift_entity_list[urls.LANGUAGE_LIST[i]][path] = gift_entity
            language_ = urls.LANGUAGE_LIST[i]
            print("地区 = %s 表数量 = %d" % (language_.ljust(20, " "), len(gift_entity_list[language_])))


def analysis_gift_data_async(view_, force=False, show_dialog=True):
    """在后台解析配置，避免 UI 卡住在进度 0。"""
    if show_dialog:
        view_.show_progress_dialog(
            title="为便捷而生",
            message="正在解析配置表，请稍等",
            busy=True,
        )
    bridge = _ensure_bridge(view_)

    def work():
        analysis_gift_data()
        bridge.config_parsed.emit(force)

    threading.Thread(target=work, daemon=True).start()


class DownloadConfig:

    def __init__(self, view_, file_path_list, force=False):
        self.view_ = view_
        self.force = force
        self.view_.download_force = force
        self.view_.download_start_time = time.time()
        if is_downloaded_config():
            # 启动时本地已有配置：静默解析，不弹「正在解析配置表」
            analysis_gift_data_async(self.view_, force=force, show_dialog=False)
            return

        self.view_.show_progress_dialog(
            title="为便捷而生",
            message="正在下载配置文件，请稍等",
            busy=False,
        )
        # 开始下载：强制重下时覆盖本地；否则跳过已存在文件以支持断点续传
        downloader_ = downloader.Downloader(
            urls.BASE_URL, file_path_list, download_type="config", skip_existing=not force)
        downloader_.my_signal.connect(self.view_.progress_callback)
        self.view_._active_downloader = downloader_
        downloader_.run()


class DownloadIcon:

    def __init__(self, view_, force=False):
        self.view_ = view_
        if is_downloaded_icon() or not overall_gift_entity or not overall_gift_entity.item_list:
            self.view_.hide_progress_dialog()
            return

        self.view_.show_progress_dialog(
            title="为便捷而生",
            message="正在准备图片下载列表",
            busy=True,
        )
        bridge = _ensure_bridge(view_)
        items = list(overall_gift_entity.item_list)

        def prep():
            file_path_list = []
            seen = set()
            dirs_needed = set()
            for item in items:
                for path in (item.icon_image_path, item.poster_path):
                    if not path or path in seen:
                        continue
                    seen.add(path)
                    file_path_list.append(path)
                    dirs_needed.add(os.path.dirname(path_pro.get_download() + path))
            for dir_path in dirs_needed:
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
            bridge.icon_list_ready.emit(file_path_list, force)

        threading.Thread(target=prep, daemon=True).start()


def is_downloaded_config():
    return json_pro.get_config_download_time() > 0


def is_downloaded_icon():
    return json_pro.get_icon_download_time() > 0
