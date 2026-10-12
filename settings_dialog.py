from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QDialog, QLabel, QStyle, QStyleOptionSlider

import settings_ui
from util import icon, ui_scale


class QSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(QSettingsDialog, self).__init__(parent)
        self.ui = settings_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(icon.get_logo())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._scale_apply_busy = False
        self._init_scale_slider()

    def _init_scale_slider(self):
        """显示比例滑动条（推荐值±0.3，步长 0.05，下限 1.0）。"""
        self._scale_steps = ui_scale.get_scale_steps()
        index = ui_scale.current_scale_index(self._scale_steps)
        self.ui.scale_slider.blockSignals(True)
        self.ui.scale_slider.setMinimum(0)
        self.ui.scale_slider.setMaximum(len(self._scale_steps) - 1)
        self.ui.scale_slider.setSingleStep(1)
        self.ui.scale_slider.setPageStep(1)
        self.ui.scale_slider.setTickInterval(1)
        self.ui.scale_slider.setValue(index)
        self.ui.scale_slider.blockSignals(False)
        self._init_scale_tick_labels()
        self._update_scale_value_label(index)
        self.ui.scale_slider.valueChanged.connect(self._on_scale_slider_changed)
        self.ui.scale_slider.sliderReleased.connect(self._apply_scale_from_slider)
        self.ui.scale_slider.installEventFilter(self)

    def _init_scale_tick_labels(self):
        """滑块下方显示可点击的比例数值（每 0.1 一档，避免 1.0~2.0 过密）。"""
        self._scale_tick_labels = []
        for i, step in enumerate(self._scale_steps):
            # 仅标注 1.0 / 1.1 / … / 2.0
            if abs(round(step * 10) - step * 10) > 1e-6:
                continue
            label = QLabel(ui_scale.format_scale(step), self.ui.scale_frame)
            label.setAlignment(Qt.AlignCenter)
            label.setCursor(Qt.PointingHandCursor)
            label.scale_index = i
            label.installEventFilter(self)
            self._scale_tick_labels.append(label)
        self._layout_scale_tick_labels()

    def _layout_scale_tick_labels(self):
        slider = self.ui.scale_slider
        if not getattr(self, "_scale_tick_labels", None):
            return
        s = ui_scale.get_applied_scale()
        label_w, label_h = max(22, int(round(34 * s))), max(12, int(round(16 * s)))
        y = slider.geometry().bottom() + max(1, int(round(2 * s)))
        opt = QStyleOptionSlider()
        for label in self._scale_tick_labels:
            index = getattr(label, "scale_index", 0)
            slider.initStyleOption(opt)
            opt.sliderPosition = index
            opt.sliderValue = index
            handle = slider.style().subControlRect(
                QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, slider)
            center_x = slider.x() + handle.center().x()
            label.setGeometry(center_x - label_w // 2, y, label_w, label_h)
            label.show()

    def _scale_index_from_pos(self, pos):
        """根据滑块点击坐标映射到最近档位下标。"""
        slider = self.ui.scale_slider
        opt = QStyleOptionSlider()
        slider.initStyleOption(opt)
        return QStyle.sliderValueFromPosition(
            slider.minimum(),
            slider.maximum(),
            pos.x(),
            slider.width(),
            opt.upsideDown,
        )

    def _select_scale_index(self, index):
        index = max(self.ui.scale_slider.minimum(),
                    min(self.ui.scale_slider.maximum(), int(index)))
        if self.ui.scale_slider.value() == index:
            self._apply_scale_from_slider()
            return
        self.ui.scale_slider.setValue(index)

    def eventFilter(self, obj, event):
        slider = getattr(self.ui, "scale_slider", None)
        if slider is not None and obj is slider:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                opt = QStyleOptionSlider()
                slider.initStyleOption(opt)
                handle = slider.style().subControlRect(
                    QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, slider)
                if not handle.contains(event.pos()):
                    self._select_scale_index(self._scale_index_from_pos(event.pos()))
                    return True
            elif event.type() == QEvent.Resize:
                self._layout_scale_tick_labels()
        labels = getattr(self, "_scale_tick_labels", None)
        if labels and obj in labels:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self._select_scale_index(obj.scale_index)
                return True
        return super(QSettingsDialog, self).eventFilter(obj, event)

    def _update_scale_value_label(self, index):
        self.ui.scale_value.setText(ui_scale.format_scale(self._scale_steps[index]))
        labels = getattr(self, "_scale_tick_labels", None)
        if not labels:
            return
        s = ui_scale.get_applied_scale()
        for label in labels:
            if getattr(label, "scale_index", -1) == index:
                css = 'font: 8pt "微软雅黑"; color: rgb(57, 61, 255); font-weight: bold;'
            else:
                css = 'font: 8pt "微软雅黑"; color: rgb(90, 90, 90);'
            label.setStyleSheet(ui_scale.scale_stylesheet(css, s))

    def _on_scale_slider_changed(self, index):
        self._update_scale_value_label(index)
        if not self.ui.scale_slider.isSliderDown():
            self._apply_scale_from_slider()

    def _restore_scale_slider(self):
        old_index = ui_scale.current_scale_index(self._scale_steps)
        self.ui.scale_slider.blockSignals(True)
        self.ui.scale_slider.setValue(old_index)
        self.ui.scale_slider.blockSignals(False)
        self._update_scale_value_label(old_index)

    def _can_apply_scale(self):
        """检查模式下改比例前先处理未保存修改。"""
        parent = self.parent()
        edit_gift = getattr(parent, "edit_gift_widget", None) if parent is not None else None
        if edit_gift is None:
            return True
        try:
            from app.edit_gift.gui import edit_gift_widget as egw
            if egw.select_mode_type != 0 and not edit_gift.ensure_unsaved_handled():
                return False
        except Exception:
            pass
        return True

    def _apply_scale_from_slider(self):
        """实时应用显示比例，无需重启。"""
        if getattr(self, "_scale_apply_busy", False):
            return
        index = self.ui.scale_slider.value()
        scale = self._scale_steps[index]
        if abs(scale - ui_scale.get_applied_scale()) < 1e-6:
            return
        self._scale_apply_busy = True
        try:
            if not self._can_apply_scale():
                self._restore_scale_slider()
                return
            ui_scale.save_scale(scale)
            window = self.parent()
            if window is None:
                window = self.window()
            was_maximized = window.isMaximized() if window is not None else False
            if window is not None and window is not self:
                ui_scale.apply_ui_scale(window, scale)
                if hasattr(window, "refresh_after_ui_scale"):
                    window.refresh_after_ui_scale()
            # 弹框可能已作为主窗口子控件被缩放；再抛光一次并恢复固定尺寸
            ui_scale.apply_ui_scale(self, scale, bump_generation=False)
            self._restore_dialog_fixed_size(scale)
            if window is not None and was_maximized:
                window.setWindowState(window.windowState() | Qt.WindowMaximized)
            self._layout_scale_tick_labels()
            self._update_scale_value_label(index)
        finally:
            self._scale_apply_busy = False

    # 与 settings_ui 设计稿一致
    _DESIGN_WIDTH = 720
    _DESIGN_HEIGHT = 540

    def _restore_dialog_fixed_size(self, scale):
        """按设计稿尺寸恢复弹框固定大小，防止改比例后内容被裁切。"""
        self.setFixedSize(
            max(1, int(round(self._DESIGN_WIDTH * scale))),
            max(1, int(round(self._DESIGN_HEIGHT * scale))),
        )

    def showEvent(self, event):
        super(QSettingsDialog, self).showEvent(event)
        self._restore_dialog_fixed_size(ui_scale.get_applied_scale())
        # 每次打开时同步当前比例档位
        index = ui_scale.current_scale_index(self._scale_steps)
        self.ui.scale_slider.blockSignals(True)
        self.ui.scale_slider.setValue(index)
        self.ui.scale_slider.blockSignals(False)
        self._layout_scale_tick_labels()
        self._update_scale_value_label(index)
