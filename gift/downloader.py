import requests

from multiprocessing.pool import ThreadPool
from PyQt5.QtCore import QObject, pyqtSignal

import utils.path_


class Downloader(QObject):
    my_signal = pyqtSignal(dict)

    def __init__(self, server_url, file_path_list, download_type="icon", parent=None):
        super(Downloader, self).__init__(parent)
        self.server_url = server_url
        self.file_path_list = file_path_list
        self.download_type = download_type

        self.downloaded_success = True
        self.downloaded_count = 0

    def down(self, file_path):
        # print("正在下载 线程名称 = %s" % threading.currentThread().name)
        try:
            file_url = self.server_url + file_path
            r = requests.get(file_url)
            with open(utils.path_.get_download() + file_path, "wb+") as fp:
                fp.write(r.content)
        except Exception as e:
            self.downloaded_success = False
            print("下载出错 URL = %s" % (self.server_url + file_path))
            print(e)
        self.downloaded_count = self.downloaded_count + 1
        value = self.downloaded_count / len(self.file_path_list) * 100
        self.my_signal.emit({"value": value, "success": self.downloaded_success, "type": self.download_type})

    def run(self):
        self.downloaded_count = 0
        ThreadPool(32).imap_unordered(self.down, self.file_path_list)
