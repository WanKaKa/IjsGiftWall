import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from bundle_meta import APP_EXE_NAME, APP_VERSION, BUNDLE_SHA256, CACHE_DIR_NAME
except ImportError:
    from version import APP_EXE_NAME, APP_VERSION, CACHE_DIR_NAME
    BUNDLE_SHA256 = ''


def _bundle_path():
    if getattr(sys, 'frozen', False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent / 'build'
    return base / 'bundle.zip'


def _cache_root():
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        local_app_data = str(Path.home() / 'AppData' / 'Local')
    return Path(local_app_data) / 'IJoySoft' / CACHE_DIR_NAME


def _cache_dir():
    return _cache_root() / APP_VERSION


def _bundle_hash_file(cache_dir):
    return cache_dir / 'bundle.sha256'


def _is_cache_ready(cache_dir):
    app_exe = cache_dir / f'{APP_EXE_NAME}.exe'
    hash_file = _bundle_hash_file(cache_dir)
    if not app_exe.exists() or not hash_file.exists():
        return False
    if not BUNDLE_SHA256:
        return True
    return hash_file.read_text(encoding='utf-8').strip() == BUNDLE_SHA256


def _cleanup_old_caches(keep_dir):
    cache_root = _cache_root()
    if not cache_root.exists():
        return
    for child in cache_root.iterdir():
        if child.is_dir() and child.resolve() != keep_dir.resolve():
            shutil.rmtree(child, ignore_errors=True)


def _extract_bundle(cache_dir):
    bundle = _bundle_path()
    if not bundle.exists():
        raise FileNotFoundError(f'未找到内置资源包: {bundle}')

    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(bundle) as archive:
        archive.extractall(cache_dir)

    if BUNDLE_SHA256:
        _bundle_hash_file(cache_dir).write_text(BUNDLE_SHA256, encoding='utf-8')
    _cleanup_old_caches(cache_dir)


def _launch_app(app_exe):
    result = subprocess.run([str(app_exe)], cwd=str(app_exe.parent))
    return result.returncode


def main():
    cache_dir = _cache_dir()
    if not _is_cache_ready(cache_dir):
        _extract_bundle(cache_dir)

    app_exe = cache_dir / f'{APP_EXE_NAME}.exe'
    if not app_exe.exists():
        raise FileNotFoundError(f'未找到程序入口: {app_exe}')

    sys.exit(_launch_app(app_exe))


if __name__ == '__main__':
    main()
