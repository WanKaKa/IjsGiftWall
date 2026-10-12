import os
import threading
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PyQt5.QtCore import QObject, pyqtSignal

from util import path_pro

# I/O 密集型：提高并发，配合连接复用显著加速 OSS 小文件批量下载
_DEFAULT_WORKERS = 32


class Downloader(QObject):
    my_signal = pyqtSignal(dict)

    def __init__(self, server_url, file_path_list, download_type="icon",
                 parent=None, max_workers=_DEFAULT_WORKERS, skip_existing=False):
        super(Downloader, self).__init__(parent)
        self.server_url = server_url
        self.file_path_list = self._dedupe(file_path_list)
        self.download_type = download_type
        self.max_workers = max_workers
        self.skip_existing = skip_existing
        self.file_path_error_list = []

        self.downloaded_success = True
        self.downloaded_count = 0
        self._lock = threading.Lock()
        self._last_emitted_count = -1
        self._worker_thread = None

    @staticmethod
    def _dedupe(file_path_list):
        seen = set()
        unique = []
        for path in file_path_list:
            if path and path not in seen:
                seen.add(path)
                unique.append(path)
        return unique

    def _make_session(self):
        """每个工作线程一个 Session，复用 TCP/TLS，避免反复握手。"""
        session = requests.Session()
        retry = Retry(
            total=2,
            connect=2,
            read=2,
            backoff_factor=0.2,
            status_forcelist=(500, 502, 503, 504),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(
            pool_connections=self.max_workers,
            pool_maxsize=self.max_workers,
            max_retries=retry,
        )
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def down(self, session, file_path):
        local_path = path_pro.get_download() + file_path
        try:
            if self.skip_existing and os.path.isfile(local_path) and os.path.getsize(local_path) > 0:
                return True
            file_url = self.server_url + file_path
            # connect / read 分离：建连快失败，读超时给足大文件
            r = session.get(file_url, timeout=(5, 30))
            r.raise_for_status()
            parent = os.path.dirname(local_path)
            if parent and not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)
            with open(local_path, "wb") as fp:
                fp.write(r.content)
            return True
        except Exception as e:
            print("下载出错 URL = %s" % (self.server_url + file_path))
            print(e)
            return False

    def _should_emit(self, count, total):
        """前几个文件每次刷新；之后按约 1% 刷新；首尾必刷。"""
        if count <= 1 or count == total:
            return True
        if total <= 200:
            return True
        step = max(1, total // 100)
        return count - self._last_emitted_count >= step

    def _on_one_done(self, file_path, ok, total):
        with self._lock:
            if not ok:
                self.downloaded_success = False
                self.file_path_error_list.append(file_path)
            self.downloaded_count += 1
            count = self.downloaded_count
            success = self.downloaded_success
            error_list = list(self.file_path_error_list)
            if not self._should_emit(count, total):
                return
            self._last_emitted_count = count
            value = 100.0 if count >= total else (count * 100.0 / total)

        label = "配置文件" if self.download_type == "config" else "图片资源"
        self.my_signal.emit({
            "value": value,
            "count": count,
            "total": total,
            "success": success,
            "type": self.download_type,
            "error_list": error_list,
            "busy": False,
            "message": "正在下载%s（%d/%d）" % (label, count, total),
        })

    def run(self):
        self.downloaded_count = 0
        self.downloaded_success = True
        self.file_path_error_list = []
        self._last_emitted_count = -1
        total = len(self.file_path_list)
        if total == 0:
            self.my_signal.emit({
                "value": 100,
                "count": 0,
                "total": 0,
                "success": True,
                "type": self.download_type,
                "error_list": [],
                "busy": False,
                "message": "没有需要下载的文件",
            })
            return

        # 立刻反馈，避免进度条长时间停在 0
        label = "配置文件" if self.download_type == "config" else "图片资源"
        self.my_signal.emit({
            "value": 0,
            "count": 0,
            "total": total,
            "success": True,
            "type": self.download_type,
            "error_list": [],
            "busy": False,
            "message": "正在连接服务器，准备下载%s（共 %d 个）" % (label, total),
        })

        workers = min(self.max_workers, total)
        file_path_list = self.file_path_list

        def worker():
            thread_local = threading.local()

            def get_session():
                session = getattr(thread_local, "session", None)
                if session is None:
                    session = self._make_session()
                    thread_local.session = session
                return session

            def task(file_path):
                ok = self.down(get_session(), file_path)
                self._on_one_done(file_path, ok, total)
                return ok

            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [executor.submit(task, path) for path in file_path_list]
                for future in futures:
                    future.result()

        self._worker_thread = threading.Thread(target=worker, daemon=True)
        self._worker_thread.start()
