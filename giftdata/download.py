import requests
from utils import path_utils
from multiprocessing.pool import ThreadPool


class Downloader:

    def __init__(self, server_url, file_path_list, progress_callback, downloaded_callback):
        self.server_url = server_url
        self.file_path_list = file_path_list
        self.progress_callback = progress_callback
        self.downloaded_callback = downloaded_callback

        self.downloaded_success = True
        self.downloaded_count = 0

    def down(self, file_path):
        self.downloaded_count = self.downloaded_count + 1
        try:
            file_url = self.server_url + file_path
            r = requests.get(file_url)
            with open(path_utils.get_download_path() + file_path, "wb+") as fp:
                fp.write(r.content)
                value = self.downloaded_count / len(self.file_path_list) * 100
                self.progress_callback(value)
        except Exception as e:
            self.downloaded_success = False
            print("下载出错 URL = %s" % (self.server_url + file_path))
            print(e)
        if self.downloaded_count == len(self.file_path_list):
            self.downloaded_callback(success=self.downloaded_success)

    def run(self):
        self.downloaded_count = 0
        ThreadPool(8).imap_unordered(self.down, self.file_path_list)
