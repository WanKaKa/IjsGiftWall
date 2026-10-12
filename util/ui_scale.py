"""界面显示比例：推荐值计算、档位选择、持久化、运行时缩放。"""
import os
import re
import sys
import weakref

# 步长 0.05；可选范围固定 1.0~2.0；默认值仍按推荐算法计算
STEP = 0.05
MIN_SCALE = 1.0
MAX_SCALE = 2.0
KEY_UI_SCALE_FACTOR = "ui_scale_factor"
# 旧版相对档位键，读取时迁移
KEY_UI_SCALE_OFFSET = "ui_scale_offset"
OFFSET_MIN = -2
OFFSET_MAX = 2

# 运行时已应用的比例（相对设计稿 1.0）
_applied_scale = 1.0
_polish_generation = 0
# id(obj) -> (weakref.ref, original metrics)；用 weakref 校验，避免控件销毁后 id 复用串数据
_widget_originals = {}
_layout_originals = {}
_QWIDGETSIZE_MAX = 16777215


def _lookup_original(store, obj):
    key = id(obj)
    entry = store.get(key)
    if entry is None:
        return None
    ref, data = entry
    if ref() is obj:
        return data
    store.pop(key, None)
    return None


def _track_original(store, obj, data):
    key = id(obj)

    def _cleanup(_ref, k=key, s=store):
        cur = s.get(k)
        if cur is not None and cur[0] is _ref:
            s.pop(k, None)

    try:
        ref = weakref.ref(obj, _cleanup)
    except TypeError:
        store[key] = (lambda: obj, data)
        try:
            obj.destroyed.connect(lambda *args, k=key, s=store: s.pop(k, None))
        except Exception:
            pass
        return data
    store[key] = (ref, data)
    return data


def read_system_scale_and_screen():
    """读取 Windows 系统缩放与主屏分辨率（可在 QApplication 创建前调用）。"""
    system_scale = 1.0
    screen_w, screen_h = 1920, 1080
    try:
        import ctypes
        user32 = ctypes.windll.user32
        try:
            system_scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
        except Exception:
            hdc = user32.GetDC(0)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            user32.ReleaseDC(0, hdc)
            system_scale = dpi / 96.0

        screen_w = int(user32.GetSystemMetrics(0)) or screen_w
        screen_h = int(user32.GetSystemMetrics(1)) or screen_h
    except Exception:
        pass
    return system_scale, screen_w, screen_h


def calc_recommended_scale():
    """根据系统缩放与分辨率计算推荐比例（夹在 1.0~2.0）。"""
    system_scale, screen_w, screen_h = read_system_scale_and_screen()
    design_w, design_h = 1400, 780
    fit_scale = min(screen_w / design_w, screen_h / design_h) * 0.92
    comfort_scale = 1.0 + max(0.0, system_scale - 1.0) * 0.4
    qt_scale = min(comfort_scale, fit_scale, 1.35)
    qt_scale = max(MIN_SCALE, min(MAX_SCALE, qt_scale))
    return _round_scale(qt_scale)


def _round_scale(value):
    """按 0.05 步长四舍五入（保留两位小数，避免浮点误差）。"""
    return round(round(float(value) / STEP) * STEP, 2)


def _clamp_scale(value, steps=None):
    """限制在 1.0~2.0 可选档位内。"""
    value = max(MIN_SCALE, min(MAX_SCALE, _round_scale(value)))
    if steps is None:
        steps = get_scale_steps()
    if not steps:
        return value
    return max(steps[0], min(steps[-1], value))


def format_scale(scale):
    """格式化为两位小数，如 1.00 / 1.05 / 1.10。"""
    return "%.2f" % max(MIN_SCALE, min(MAX_SCALE, _round_scale(scale)))


def get_scale_steps(recommended=None):
    """固定档位 1.00~2.00，步长 0.05（共 21 档）。"""
    n = int(round((MAX_SCALE - MIN_SCALE) / STEP))
    return [_round_scale(MIN_SCALE + i * STEP) for i in range(n + 1)]


def nearest_step_index(scale, steps=None):
    if steps is None:
        steps = get_scale_steps()
    target = max(MIN_SCALE, min(MAX_SCALE, _round_scale(scale)))
    best_i, best_diff = 0, abs(steps[0] - target)
    for i, value in enumerate(steps):
        diff = abs(value - target)
        if diff < best_diff:
            best_i, best_diff = i, diff
    return best_i


def get_recommended_index(steps=None, recommended=None):
    if recommended is None:
        recommended = calc_recommended_scale()
    if steps is None:
        steps = get_scale_steps()
    return nearest_step_index(recommended, steps)


def get_saved_scale():
    """读取用户保存的比例；无记录返回 None（表示用推荐值）。小于 1.0 时抬到 1.0。"""
    try:
        from database import json_pro
        data = json_pro.get()
        if not data:
            return None
        if KEY_UI_SCALE_FACTOR in data:
            return _clamp_scale(data[KEY_UI_SCALE_FACTOR])
        # 兼容旧版偏移档位
        if KEY_UI_SCALE_OFFSET in data:
            steps = get_scale_steps()
            offset = max(OFFSET_MIN, min(OFFSET_MAX, int(data[KEY_UI_SCALE_OFFSET])))
            index = max(0, min(len(steps) - 1, get_recommended_index(steps) + offset))
            return _clamp_scale(steps[index])
    except Exception:
        pass
    return None


def save_scale(scale):
    scale = _clamp_scale(scale)
    from database import json_pro
    json_pro.save(KEY_UI_SCALE_FACTOR, scale)


def current_scale_index(steps=None):
    """当前应选中的滑块下标。"""
    if steps is None:
        steps = get_scale_steps()
    saved = get_saved_scale()
    if saved is None:
        return get_recommended_index(steps)
    return nearest_step_index(saved, steps)


def resolve_scale_factor():
    """启动时最终使用的缩放（当前档位范围内，且 ≥ 1.0）。

    调试可用环境变量 IJS_QT_SCALE_FACTOR 强制覆盖。
    """
    steps = get_scale_steps()
    if "IJS_QT_SCALE_FACTOR" in os.environ:
        try:
            return _clamp_scale(os.environ["IJS_QT_SCALE_FACTOR"], steps)
        except Exception:
            pass
    return _clamp_scale(steps[current_scale_index(steps)], steps)


def apply_scale_env(scale=None):
    """启动前环境：关闭系统自动缩放；用户比例改为运行时 apply_ui_scale。"""
    if scale is None:
        scale = resolve_scale_factor()
    scale = _clamp_scale(scale)
    # 不再使用 QT_SCALE_FACTOR，以便改比例可实时生效
    os.environ.pop("QT_SCALE_FACTOR", None)
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "0")
    os.environ.setdefault("QT_FONT_DPI", "96")
    return scale


def get_applied_scale():
    return _clamp_scale(_applied_scale)


def scaled_pt(pt):
    """设计稿 pt → 当前显示比例。"""
    return max(0.5, float(pt) * get_applied_scale())


def scaled_px(px):
    """设计稿 px → 当前显示比例。"""
    return max(1, int(round(float(px) * get_applied_scale())))


def make_font(family, pt, bold=False):
    """按当前显示比例创建字体。"""
    from PyQt5.QtGui import QFont
    font = QFont(family)
    font.setPointSizeF(scaled_pt(pt))
    if bold:
        font.setBold(True)
    return font


def restart_app():
    """重启进程（兼容保留，正常改比例不再需要）。"""
    os.environ.pop("QT_SCALE_FACTOR", None)
    python = sys.executable
    os.execv(python, [python] + sys.argv)


def device_pixel_ratio(widget=None):
    """屏幕 DPR。控件逻辑尺寸已含显示比例时，勿再乘 UI scale。"""
    reported = 1.0
    try:
        from PyQt5.QtWidgets import QApplication
        if widget is not None:
            try:
                reported = float(widget.devicePixelRatioF())
            except Exception:
                reported = float(widget.devicePixelRatio())
        else:
            app = QApplication.instance()
            if app is not None:
                screen = app.primaryScreen()
                if screen is not None:
                    try:
                        reported = float(screen.devicePixelRatioF())
                    except Exception:
                        reported = float(screen.devicePixelRatio())
    except Exception:
        reported = 1.0
    return max(1.0, reported)


def scale_stylesheet(css, scale=None):
    """按比例缩放样式表中的字号与常见 px 尺寸。"""
    if not css:
        return css
    if scale is None:
        scale = get_applied_scale()
    scale = float(scale)
    if abs(scale - 1.0) < 1e-6:
        return css

    def font_repl(match):
        num = float(match.group(2)) * scale
        unit = match.group(3)
        if unit.lower() == "px":
            return "%s%dpx" % (match.group(1), max(1, int(round(num))))
        text = ("%.2f" % num).rstrip("0").rstrip(".")
        return "%s%s%s" % (match.group(1), text, unit)

    css = re.sub(
        r"(font(?:-size)?\s*:\s*(?:(?:bold|italic|normal|\d+)\s+)*)(\d+(?:\.\d+)?)(pt|px)",
        font_repl,
        css,
        flags=re.I,
    )

    def px_repl(match):
        raw = float(match.group(2))
        if raw <= 0:
            return "%s0px" % match.group(1)
        return "%s%dpx" % (match.group(1), max(1, int(round(raw * scale))))

    css = re.sub(
        r"(\b(?:padding|margin|border-radius|border(?:-width)?|spacing|"
        r"min-width|min-height|max-width|max-height|width|height)"
        r"(?:-(?:top|right|bottom|left))?\s*:\s*)(\d+)px",
        px_repl,
        css,
        flags=re.I,
    )
    return css


def _ensure_widget_original(widget):
    cached = _lookup_original(_widget_originals, widget)
    if cached is not None:
        return cached
    font = widget.font()
    min_size = widget.minimumSize()
    max_size = widget.maximumSize()
    data = {
        "font_pt": font.pointSizeF(),
        "font_px": font.pixelSize(),
        "min_w": min_size.width(),
        "min_h": min_size.height(),
        "max_w": max_size.width(),
        "max_h": max_size.height(),
        "stylesheet": widget.styleSheet() or "",
        "geom": widget.geometry(),
        "has_fixed_w": min_size.width() == max_size.width() and 0 < min_size.width() < _QWIDGETSIZE_MAX,
        "has_fixed_h": min_size.height() == max_size.height() and 0 < min_size.height() < _QWIDGETSIZE_MAX,
    }
    try:
        from PyQt5.QtWidgets import QAbstractItemView, QTableView, QTreeView, QListView
        if isinstance(widget, QAbstractItemView):
            icon = widget.iconSize()
            data["icon_w"] = icon.width()
            data["icon_h"] = icon.height()
        if isinstance(widget, (QTableView, QTreeView, QListView)):
            header = widget.horizontalHeader() if hasattr(widget, "horizontalHeader") else None
            if header is not None:
                data["header_h"] = header.height()
    except Exception:
        pass
    return _track_original(_widget_originals, widget, data)


def _ensure_layout_original(layout):
    cached = _lookup_original(_layout_originals, layout)
    if cached is not None:
        return cached
    margins = layout.contentsMargins()
    data = {
        "l": margins.left(),
        "t": margins.top(),
        "r": margins.right(),
        "b": margins.bottom(),
        "spacing": layout.spacing() if hasattr(layout, "spacing") else -1,
    }
    return _track_original(_layout_originals, layout, data)


def _is_free_geometry(widget):
    parent = widget.parentWidget()
    if parent is None:
        return False
    if parent.layout() is not None:
        return False
    return True


def _apply_one_widget(widget, scale):
    from PyQt5.QtCore import QSize
    from PyQt5.QtWidgets import QAbstractItemView, QTableView, QTreeView, QListView

    orig = _ensure_widget_original(widget)
    font = widget.font()
    if orig["font_pt"] > 0:
        font.setPointSizeF(max(0.5, orig["font_pt"] * scale))
        widget.setFont(font)
    elif orig["font_px"] > 0:
        font.setPixelSize(max(1, int(round(orig["font_px"] * scale))))
        widget.setFont(font)

    if orig["stylesheet"]:
        widget.setStyleSheet(scale_stylesheet(orig["stylesheet"], scale))

    # 无父级的顶层主窗口不改尺寸约束/几何，避免冲掉最大化
    is_top_level = widget.isWindow() and widget.parentWidget() is None
    if not is_top_level:
        min_w = orig["min_w"]
        min_h = orig["min_h"]
        max_w = orig["max_w"]
        max_h = orig["max_h"]
        if min_w > 0:
            min_w = max(1, int(round(min_w * scale)))
        if min_h > 0:
            min_h = max(1, int(round(min_h * scale)))
        if 0 < max_w < _QWIDGETSIZE_MAX:
            max_w = max(1, int(round(max_w * scale)))
        if 0 < max_h < _QWIDGETSIZE_MAX:
            max_h = max(1, int(round(max_h * scale)))
        widget.setMinimumSize(min_w, min_h)
        widget.setMaximumSize(max_w, max_h)
        if orig["has_fixed_w"] and orig["has_fixed_h"]:
            widget.setFixedSize(min_w, min_h)
        elif orig["has_fixed_w"]:
            widget.setFixedWidth(min_w)
        elif orig["has_fixed_h"]:
            widget.setFixedHeight(min_h)

        if _is_free_geometry(widget):
            g = orig["geom"]
            widget.setGeometry(
                int(round(g.x() * scale)),
                int(round(g.y() * scale)),
                max(1, int(round(g.width() * scale))),
                max(1, int(round(g.height() * scale))),
            )

    if isinstance(widget, QAbstractItemView) and "icon_w" in orig:
        widget.setIconSize(QSize(
            max(1, int(round(orig["icon_w"] * scale))),
            max(1, int(round(orig["icon_h"] * scale))),
        ))
    if isinstance(widget, (QTableView, QTreeView, QListView)) and "header_h" in orig:
        header = widget.horizontalHeader()
        if header is not None and orig["header_h"] > 0:
            header.setFixedHeight(max(1, int(round(orig["header_h"] * scale))))


def _apply_one_layout(layout, scale):
    orig = _ensure_layout_original(layout)
    layout.setContentsMargins(
        int(round(orig["l"] * scale)),
        int(round(orig["t"] * scale)),
        int(round(orig["r"] * scale)),
        int(round(orig["b"] * scale)),
    )
    if orig["spacing"] >= 0 and hasattr(layout, "setSpacing"):
        layout.setSpacing(int(round(orig["spacing"] * scale)))


def _walk_apply(widget, scale, seen_layouts):
    from PyQt5.QtWidgets import QWidget, QLayout

    if widget is None:
        return
    _apply_one_widget(widget, scale)
    layout = widget.layout()
    if isinstance(layout, QLayout) and id(layout) not in seen_layouts:
        seen_layouts.add(id(layout))
        _apply_one_layout(layout, scale)
    for child in widget.children():
        if isinstance(child, QWidget):
            _walk_apply(child, scale, seen_layouts)


def apply_ui_scale(root, scale=None, bump_generation=True):
    """将 root 及其子控件缩放到指定比例（相对设计稿绝对值，可重复调用）。"""
    global _applied_scale, _polish_generation
    if root is None:
        return get_applied_scale()
    if scale is None:
        scale = resolve_scale_factor()
    scale = _clamp_scale(scale)
    _walk_apply(root, scale, set())
    # 仅对无父窗口的顶层主窗口放开尺寸约束，避免冲掉最大化；
    # 有父级的对话框需保留设计稿固定尺寸，否则改比例后内容会被裁切消失
    try:
        from PyQt5.QtWidgets import QLayout
        layout = root.layout()
        if layout is not None:
            layout.setSizeConstraint(QLayout.SetNoConstraint)
        if root.isWindow() and root.parentWidget() is None:
            root.setMinimumSize(0, 0)
            root.setMaximumSize(_QWIDGETSIZE_MAX, _QWIDGETSIZE_MAX)
    except Exception:
        pass
    _applied_scale = scale
    if bump_generation:
        _polish_generation += 1
        try:
            root._ui_scale_gen = _polish_generation
        except Exception:
            pass
    return scale


def polish_window(window):
    """顶层窗口显示时按当前比例抛光（避免对话框仍是 1.0）。"""
    if window is None:
        return
    try:
        if getattr(window, "_ui_scale_gen", None) == _polish_generation:
            return
    except Exception:
        pass
    apply_ui_scale(window, get_applied_scale(), bump_generation=False)
    try:
        window._ui_scale_gen = _polish_generation
    except Exception:
        pass


def _as_qsize(logical_w, logical_h=None):
    from PyQt5.QtCore import QSize
    if logical_h is None:
        if hasattr(logical_w, "width") and hasattr(logical_w, "height"):
            return QSize(max(1, int(logical_w.width())), max(1, int(logical_w.height())))
        side = max(1, int(logical_w))
        return QSize(side, side)
    return QSize(max(1, int(logical_w)), max(1, int(logical_h)))


def scaled_pixmap(source, logical_w, logical_h=None, widget=None, keep_ratio=True):
    """按逻辑尺寸 × DPR 生成清晰 QPixmap，并设置 devicePixelRatio。"""
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap

    size = _as_qsize(logical_w, logical_h)
    if isinstance(source, QPixmap):
        pixmap = source
    else:
        pixmap = QPixmap(str(source))
    if pixmap.isNull():
        return pixmap

    dpr = device_pixel_ratio(widget)
    target = _as_qsize(size.width() * dpr, size.height() * dpr)
    aspect = Qt.KeepAspectRatio if keep_ratio else Qt.IgnoreAspectRatio
    scaled = pixmap.scaled(target, aspect, Qt.SmoothTransformation)
    scaled.setDevicePixelRatio(dpr)
    return scaled


def scaled_icon(source, logical_w, logical_h=None, widget=None):
    """生成适合当前缩放比例的 QIcon（表格图标等）。"""
    from PyQt5.QtGui import QIcon
    return QIcon(scaled_pixmap(source, logical_w, logical_h, widget=widget))


def set_label_pixmap(label, source, logical_w=None, logical_h=None, keep_ratio=True):
    """给 QLabel 设置按 DPR 缩放的图片，并关闭 scaledContents 以免二次拉伸发糊。"""
    if label is None:
        return
    if logical_w is None:
        size = label.size()
        if size.width() < 1 or size.height() < 1:
            size = label.maximumSize()
        logical_w, logical_h = size.width(), size.height()
    label.setScaledContents(False)
    label.setPixmap(scaled_pixmap(source, logical_w, logical_h, widget=label, keep_ratio=keep_ratio))
