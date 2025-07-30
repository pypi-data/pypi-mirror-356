from abc import abstractmethod
from collections.abc import Callable
import math
from typing import override
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QSizePolicy, QToolButton, QWidget, QGridLayout, QLabel, QComboBox, QColorDialog, QCheckBox, QPushButton, QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout, QGroupBox, QLineEdit, QStackedLayout, QButtonGroup, QDial, QStyle
import pyqtgraph as pg
import numpy as np
import sys
import signal

GRID_SIZE = 30

class Toast(QtWidgets.QLabel):
    closed = QtCore.pyqtSignal()

    COLORS = {
        "success": "#4caf50",
        "warning": "#ffb300",
        "error": "#e53935",
        "info": "#333"
    }

    ICONS = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }

    def __init__(self, parent: QWidget, message:str, duration:int, stack_index, level="info"):
        super().__init__(parent)
        icon = self.ICONS.get(level, "")
        color = self.COLORS.get(level, "#333")

        self.setText(f"{icon} {message}")
        self.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint |
                            QtCore.Qt.WindowType.ToolTip)
        self.adjustSize()
        self.stack_index = stack_index
        self.reposition(stack_index)
        self.show()

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.timer.start(duration)

    def reposition(self, stack_index):
        parent_geo = self.parent().geometry()
        x = parent_geo.width() - self.width() - 20
        y = parent_geo.height() - self.height() - 20 - stack_index * (self.height() + 10)
        self.move(x, y)

    def mousePressEvent(self, event):
        self.close()

    def close(self):
        if self.isVisible():
            super().close()
            self.closed.emit()

class ToastManager:
    def __init__(self, parent: QWidget):
        self.parent: QWidget = parent
        self.toasts: list[Toast] = []

    def show(self, message:str, duration:int=3000, level:str="info"):
        toast = Toast(self.parent, message, duration, len(self.toasts), level)
        toast.closed.connect(lambda: self._remove_toast(toast))
        self.toasts.append(toast)

    def _remove_toast(self, toast:Toast):
        if toast in self.toasts:
            self.toasts.remove(toast)
            self._reposition_toasts()

    def _reposition_toasts(self):
        for i, toast in enumerate(self.toasts):
            toast.reposition(i)

class Device:
    def __init__(self, name: str, plot_item: pg.PlotItem, x: np.ndarray, config_widget):
        self.name = name
        self.data = np.zeros_like(x, dtype=float)
        self.color = 'y'
        self.mode = 'Sinus'
        self.curve = plot_item.plot(pen=self.color, name=name)
        self.config_widget = config_widget
        self.step = 0

class TriStateBitButton(QToolButton):
    STATES = [
        ("?", None),
        ("0", QColor("red")),
        ("1", QColor("green"))
    ]

    def __init__(self, bit_index: int):
        super().__init__()
        self.bit_index = bit_index
        self.state_index = 0
        self.setCheckable(True)
        self.setFixedSize(16,16)
        self.setToolTip(f"Bit {bit_index}")
        self.update_state()
        self.clicked.connect(self.next_state)

    def next_state(self):
        self.state_index = (self.state_index + 1) % 3
        self.update_state()

    def update_state(self):
        text, color = self.STATES[self.state_index]
        self.setText(text)
        bg = color.name() if color else "none"
        self.setStyleSheet(f"""
            QToolButton {{
                border: 1px solid gray;
            }}
        """)

    def get_state(self):
        return ["dontcare", "0", "1"][self.state_index]


class BitGrid(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = []
        for i in range(9):
            btn = TriStateBitButton(bit_index=i)
            self.buttons.append(btn)
            row, col = divmod(i, 3)
            layout.addWidget(btn, row, col)

        self.setLayout(layout)

    def get_bitmask(self):
        return [btn.get_state() for btn in self.buttons]

def pretty_prefix(x: float):
    """Give the number an appropriate SI prefix.

    :param x: Too big or too small number.
    :returns: String containing a number between 1 and 1000 and SI prefix.
    """
    if x == 0:
        return "0  "

    l = math.floor(math.log10(abs(x)))

    div, mod = divmod(l, 3)
    return "%.3g %s" % (x * 10**(-l + mod), " kMGTPEZYyzafpnµm"[div])

def format_engineering(value: float, sigfigs: int) -> tuple[str, int]:
    if value == 0:
        return ("0", 0)

    sign = "-" if value < 0 else ""
    abs_val = abs(value)

    exponent = int(math.floor(math.log10(abs_val)))
    eng_exponent = 3 * (exponent // 3)
    scaled: float = abs_val / (10 ** eng_exponent)

    # Round to significant figures
    digits = sigfigs - int(math.floor(math.log10(scaled))) - 1
    rounded = round(scaled, digits)

    # Format and strip trailing junk
    mantissa = f"{rounded:.{digits}f}".rstrip("0").rstrip(".")
    return (sign + mantissa, eng_exponent)


class Knob(QWidget):
    def __init__(self, title: str, unit: str, steps: int):
        super().__init__()
        self.setFixedSize(GRID_SIZE*2, GRID_SIZE*2)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)


        title_label = QLabel(title)
        layout.addWidget(title_label)
        font = title_label.font()
        font.setPointSize(int(GRID_SIZE * 0.3))
        title_label.setFont(font)

        self._dial = QDial()
        self._dial.setMinimum(0)
        self._dial.setMaximum(steps - 1)
        self._dial.setFixedSize(int(GRID_SIZE*1), int(GRID_SIZE*1))

        dial_layout = QHBoxLayout()
        dial_layout.setContentsMargins(0, 0, 0, 0)
        dial_layout.setSpacing(0)
        dial_layout.addStretch()
        dial_layout.addWidget(self._dial)
        dial_layout.addStretch()
        layout.addLayout(dial_layout)

        dial_label = QLabel(" (mV):")
        dial_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        dial_label.setContentsMargins(0, 0, 0, 0)
        dial_label.setFont(font)
        layout.addWidget(dial_label)

        self._dial.valueChanged.connect(lambda v: dial_label.setText(f"{pretty_prefix(self._step_to_value(v))}{unit}"))
    
    def setValue(self, a0: float):
        self._dial.setValue(self._value_to_step(a0))
    
    def onValueChanged(self, slot: Callable[[float], None]):
        def f(value: int):
            v = self._step_to_value(value)
            slot(v)
        self._dial.valueChanged.connect(f)

    @abstractmethod
    def _step_to_value(self, step: int) -> float:
        return NotImplemented

    @abstractmethod
    def _value_to_step(self, value: float) -> int:
        return NotImplemented
    
class LinearKnob(Knob):
    def __init__(self, title: str, unit: str, lower_limit: float, upper_limit: float, steps: int=1321):
        super().__init__(title, unit, steps)
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit

    def _step_to_value(self, step: int) -> float:
        return step / self._dial.maximum() * (self._upper_limit - self._lower_limit) + self._lower_limit

    def _value_to_step(self, value: float) -> int:
        return int((value - self._lower_limit) / (self._upper_limit - self._lower_limit) * self._dial.maximum())

    def setLimits(self, lower_limit: float, upper_limit: float):
        self._lower_limit = lower_limit
        self._upper_limit = upper_limit

class LogKnob(Knob):
    def __init__(self, title: str, unit: str, min_exp: float, max_exp: float, steps: int=1321):
        super().__init__(title, unit, steps)
        self._min_exp = min_exp
        self._max_exp = max_exp

    def _step_to_value(self, step: int) -> float:
        return 2** (step / self._dial.maximum() * (self._max_exp - self._min_exp) + self._min_exp)

    def _value_to_step(self, value: float) -> int:
        return int((math.log(value, 2) - self._min_exp) / (self._max_exp - self._min_exp) * self._dial.maximum())
    
class QuadraticKnob(LinearKnob):
    def __init__(self, title: str, unit: str, lower_limit: float, upper_limit: float, steps: int=1321):
        self._lower_is_negative = lower_limit < 0
        self._upper_is_negative = upper_limit < 0

        sqrt_lower = math.sqrt(abs(lower_limit)) * (-1 if self._lower_is_negative else 1)
        sqrt_upper = math.sqrt(abs(upper_limit)) * (-1 if self._upper_is_negative else 1)
        super().__init__(title, unit, sqrt_lower, sqrt_upper, steps)

    def _step_to_value(self, step: int) -> float:
        v = super()._step_to_value(step)
        return v**2 if v >= 0 else -(v**2)

    def _value_to_step(self, value: float) -> int:
        sqrt_value = math.sqrt(abs(value)) * (-1 if value < 0 else 1)
        return super()._value_to_step(sqrt_value)

class WaveformSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0,0,0,0)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        trigger_mode_group = QButtonGroup(self)
        trigger_mode_group.setExclusive(True)

        sine_button = QToolButton()
        sine_button.setText("Si")

        square_button = QToolButton()
        square_button.setText("Sq")

        triangle_button = QToolButton()
        triangle_button.setText("️T")

        ekg_button = QToolButton()
        ekg_button.setText("E")

        for btn in (sine_button, square_button, triangle_button, ekg_button):
            btn.setMinimumSize(GRID_SIZE, GRID_SIZE)
            btn.setMaximumSize(GRID_SIZE, GRID_SIZE)
            btn.setCheckable(True)
            trigger_mode_group.addButton(btn)
        
        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(0)
        row1.addWidget(sine_button)
        row1.addWidget(square_button)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(0)
        row2.addWidget(triangle_button)
        row2.addWidget(ekg_button)
        sine_button.setChecked(True)

        layout.addLayout(row1)
        layout.addLayout(row2)

        self.dial = LinearKnob("Frequency", "Hz", 0.1, 10000)
        self.dial.setValue(10)

        layout.addWidget(self.dial)
    
class DigitalChannelSelectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        size = int(GRID_SIZE * 2 / 3)

        self.buttons = []
        for i in range(9):
            btn = QToolButton()
            btn.setCheckable(True)
            btn.setText(str(i))
            btn.setFixedSize(size, size)
            self.buttons.append(btn)
            row, col = divmod(i, 3)
            layout.addWidget(btn, row, col)

        self.setLayout(layout)

class AnalogTriggerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0,0,0,0)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        trigger_mode_group = QButtonGroup(self)
        trigger_mode_group.setExclusive(True)

        analog_level_time = QToolButton()
        analog_level_time.setText("↩️")

        analog_rising = QToolButton()
        analog_rising.setText("↗️")

        analog_level = QToolButton()
        analog_level.setText("➡️️")

        analog_falling = QToolButton()
        analog_falling.setText("↘️")

        for btn in (analog_level_time, analog_rising, analog_level, analog_falling):
            btn.setMinimumSize(GRID_SIZE, GRID_SIZE)
            btn.setMaximumSize(GRID_SIZE, GRID_SIZE)
            btn.setCheckable(True)
            trigger_mode_group.addButton(btn)
        
        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(0)
        row1.addWidget(analog_level_time)
        row1.addWidget(analog_rising)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(0)
        row2.addWidget(analog_level)
        row2.addWidget(analog_falling)
        analog_level_time.setChecked(True)

        layout.addLayout(row1)
        layout.addLayout(row2)

        self.dial = LinearKnob("Level", "V", -66, 66)
        self.dial.setValue(10)

        layout.addWidget(self.dial)

class DigitalTriggerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        layout = QVBoxLayout()
        self.setContentsMargins(0,0,0,0)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        trigger_mode_group = QButtonGroup(self)
        trigger_mode_group.setExclusive(True)

        analog_level_time = QToolButton()
        analog_level_time.setText("↩️")

        analog_rising = QToolButton()
        analog_rising.setText("↗️")

        analog_level = QToolButton()
        analog_level.setText("➡️️")

        analog_falling = QToolButton()
        analog_falling.setText("↘️")

        for btn in (analog_level_time, analog_rising, analog_level, analog_falling):
            btn.setMinimumSize(GRID_SIZE, GRID_SIZE)
            btn.setMaximumSize(GRID_SIZE, GRID_SIZE)
            btn.setCheckable(True)
            trigger_mode_group.addButton(btn)
        
        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(0)
        row1.addWidget(analog_level_time)
        row1.addWidget(analog_rising)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(0)
        row2.addWidget(analog_level)
        row2.addWidget(analog_falling)
        analog_level_time.setChecked(True)

        layout.addLayout(row1)
        layout.addLayout(row2)

        self.bit_grid = BitGrid()

        layout.addWidget(self.bit_grid)
        self.setLayout(layout)

# --- Combined Main Widget ---
class TriggerConfigWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        main_layout = QGridLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        led = QLabel("🔴")
        main_layout.addWidget(led, 0, 0, 1, 1)

        rename_button = QToolButton()
        rename_button.setText("R")
        rename_button.setFixedSize(GRID_SIZE, GRID_SIZE)
        main_layout.addWidget(rename_button, 1, 0)

        transport_control = QStackedLayout()
        controls_when_paused_l = QHBoxLayout()
        controls_when_paused_l.setContentsMargins(0, 0, 0, 0)
        controls_when_paused_l.setSpacing(0)
        controls_when_paused_w = QWidget()
        controls_when_paused_w.setLayout(controls_when_paused_l)

        play_button = QToolButton()
        play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        play_button.setToolTip("Continously sample")
        play_button.setFixedSize(GRID_SIZE, GRID_SIZE)
        controls_when_paused_l.addWidget(play_button)

        step_button = QToolButton()
        step_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        step_button.setToolTip("Capture one sample")
        step_button.setFixedSize(GRID_SIZE, GRID_SIZE)
        controls_when_paused_l.addWidget(step_button)

        pause_button = QToolButton()
        pause_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        pause_button.setToolTip("Pause sampling")
        pause_button.setFixedSize(2*GRID_SIZE, GRID_SIZE)

        transport_control.addWidget(controls_when_paused_w)
        transport_control.addWidget(pause_button)

        transport_control.setCurrentIndex(1)

        main_layout.addLayout(transport_control, 0, 1, 1, 2)

        time_frame_dial = LogKnob("Capture", "s", -13, 1.5)
        time_frame_dial.setValue(0.1)
        delay_dial = QuadraticKnob("Delay", "s", 0, 1)
        delay_dial.setValue(0.1)
        delay_dial.setValue(0)

        main_layout.addWidget(time_frame_dial, 2, 0, 2, 2)
        main_layout.addWidget(delay_dial, 2, 2, 2, 2)

        # Trigger mode selector (Analog / Digital)
        self.analog_btn = QPushButton("A")
        self.digital_btn = QPushButton("D")

        for btn in (self.analog_btn, self.digital_btn):
            btn.setCheckable(True)
            btn.setFixedWidth(GRID_SIZE)
            btn.setFixedHeight(GRID_SIZE)
            btn.setContentsMargins(0, 0, 0, 0)

        mode_group = QButtonGroup(self)
        mode_group.setExclusive(True)
        mode_group.addButton(self.analog_btn)
        mode_group.addButton(self.digital_btn)
        self.analog_btn.setChecked(True)

        main_layout.addWidget(self.analog_btn, 0, 3, 1, 1)
        main_layout.addWidget(self.digital_btn, 1,3, 1, 1)

        # Stacked mode-specific layout
        self.value_stack = QStackedLayout()
        self.value_stack.addWidget(AnalogTriggerPanel())
        self.value_stack.addWidget(DigitalTriggerPanel())
        stack_container = QWidget()
        stack_container.setLayout(self.value_stack)
        stack_container.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        main_layout.addWidget(stack_container, 0, 4, 4, 2)

        # Button logic
        self.analog_btn.clicked.connect(lambda: self.value_stack.setCurrentIndex(0))
        self.digital_btn.clicked.connect(lambda: self.value_stack.setCurrentIndex(1))

        main_layout.addWidget(WaveformSelector(), 0, 6, 4, 2)

        main_layout.addWidget(DigitalChannelSelectorWidget(), 2, 8, 2, 2)

        bnc_button = QToolButton()
        bnc_button.setText("P")
        bnc_button.setFixedSize(GRID_SIZE, GRID_SIZE)
        bnc_button.setCheckable(True)
        main_layout.addWidget(bnc_button, 3, 10)
        bnc_button.setChecked(True)

        x1_button = QToolButton()
        x1_button.setText("x1")
        x1_button.setFixedSize(GRID_SIZE, GRID_SIZE)
        x1_button.setCheckable(True)
        main_layout.addWidget(x1_button, 0, 8)

        x10_button = QToolButton()
        x10_button.setText("x10")
        x10_button.setCheckable(True)
        x10_button.setFixedSize(GRID_SIZE, GRID_SIZE)
        main_layout.addWidget(x10_button, 1, 8)

        buttongroup = QButtonGroup(self)
        buttongroup.setExclusive(True)
        buttongroup.addButton(x1_button)
        buttongroup.addButton(x10_button)
        x1_button.setChecked(True)

        cal_0v = QToolButton()
        cal_0v.setText("0V")
        cal_0v.setFixedSize(GRID_SIZE, GRID_SIZE)
        main_layout.addWidget(cal_0v, 0, 9)

        cal_3v3 = QToolButton()
        cal_3v3.setText("3.3")
        cal_3v3.setFixedSize(GRID_SIZE, GRID_SIZE)
        main_layout.addWidget(cal_3v3, 1, 9)

        delete_button = QToolButton()
        delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        delete_button.setToolTip("Remove device")
        delete_button.setFixedSize(GRID_SIZE, GRID_SIZE)

        main_layout.addWidget(delete_button, 0, 10)

        main_layout.addWidget(ColorButton(), 1, 10)

        save = QToolButton()
        save.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save.setToolTip("Save calibration")
        save.setFixedSize(GRID_SIZE, GRID_SIZE)

        main_layout.addWidget(save, 2, 10)


class ColorButton(QToolButton):
        # self.color_button = QtWidgets.QPushButton()
    def __init__(self):
        super().__init__()
        self.setFixedSize(GRID_SIZE, GRID_SIZE)
        self.setStyleSheet("background-color: yellow; border: 1px solid gray;")
        self.setToolTip("Pick color")
        self.clicked.connect(self.pick_color)

    def pick_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")

    def get_color(self):
        return self.palette().button().color().name()

        
class DeviceConfigWidget(QtWidgets.QGroupBox):
    def __init__(self, device_name: str, on_delete: Callable[[], None], on_config_change: Callable[[], None]):
        super().__init__()
        self.setTitle(device_name)
        self.setStyleSheet("DeviceConfigWidget { border: 1px solid #ccc; border-radius: 6px; margin-top: 20px; }")

        layout = QGridLayout()
        self.setLayout(layout)

        # 'X' icon button in the corner

        self.mode_dropdown = QtWidgets.QComboBox()
        self.mode_dropdown.addItems(["Sinus", "Random", "Flat"])
        self.mode_dropdown.currentTextChanged.connect(on_config_change)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(10)
        self.slider.valueChanged.connect(on_config_change)

        layout.addWidget(QtWidgets.QLabel("Color:"), 1, 0)
        layout.addWidget(QtWidgets.QLabel("Mode:"), 2, 0)
        layout.addWidget(self.mode_dropdown, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Noise:"), 3, 0)
        layout.addWidget(self.slider, 3, 1, 1, 2)

        sub_layout = QGridLayout()
        trigger_widget = TriggerConfigWidget()
        sub_layout.addWidget(trigger_widget, 0, 4, 1, 3)
        layout.addLayout(sub_layout, 4, 0, 1, 2)

    def get_mode(self):
        return self.mode_dropdown.currentText()

    def get_noise(self):
        return max(self.slider.value() / 10, 0.3)

class LivePlotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Plot with Device Manager")
        self.resize(1400, 800)

        self.devices: dict[str, Device] = {}
        self.device_counter = 1
        self.x = np.arange(200)
        self.toast_manager = ToastManager(self)

        main_layout = QtWidgets.QHBoxLayout(self)

        self.plot_area = pg.GraphicsLayoutWidget()
        main_layout.addWidget(self.plot_area, stretch=4)
        self.plot_layouts = []

        self.sidebar_scroll = QtWidgets.QScrollArea()
        self.sidebar_scroll.setWidgetResizable(True)
        self.sidebar_widget = QtWidgets.QWidget()
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_scroll.setWidget(self.sidebar_widget)

        main_layout.addWidget(self.sidebar_scroll, stretch=2)

        # === Device name input + add button ===
        add_row = QtWidgets.QHBoxLayout()
        self.device_name_input = QtWidgets.QLineEdit()
        self.device_name_input.setPlaceholderText("Device name")
        self.add_device_button = QtWidgets.QPushButton("+ Add Device")
        self.add_device_button.clicked.connect(self.add_device)
        add_row.addWidget(self.device_name_input)
        add_row.addWidget(self.add_device_button)

        self.sidebar_layout.addLayout(add_row)
        self.sidebar_layout.addStretch()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def add_device(self):
        typed_name = self.device_name_input.text().strip()
        name = typed_name if typed_name else f"Device {self.device_counter}"
        self.device_counter += 1
        self.device_name_input.clear()

        try:
            if name.endswith("3"):
                raise RuntimeError("Could not connect to device")

            if self.plot_layouts:
                self.plot_area.nextRow()
            plot = self.plot_area.addPlot(title=name)
            plot.showGrid(x=True, y=True)
            plot.setLabel('left', name)

            config_widget = DeviceConfigWidget(
                name,
                on_delete=lambda: self.remove_device(name),
                on_config_change=lambda: self.apply_config(name)
            )
            self.sidebar_layout.insertWidget(self.sidebar_layout.count() - 2, config_widget)

            device = Device(name, plot, self.x, config_widget)
            self.devices[name] = device
            self.plot_layouts.append(plot)

            self.toast_manager.show(f"✅ Connected to {name}", level="success")

        except Exception as e:
            self.toast_manager.show(str(e), level="error")
            print(e)

    def remove_device(self, name:str):
        device = self.devices.pop(name, None)
        if not device:
            return

        device.curve.clear()
        device.config_widget.setParent(None)
        self.rebuild_plots()

    def rebuild_plots(self):
        self.plot_area.clear()
        self.plot_layouts.clear()
        for name, device in self.devices.items():
            self.plot_area.nextRow()
            plot = self.plot_area.addPlot(title=name)
            plot.showGrid(x=True, y=True)
            plot.setLabel('left', name)
            device.curve = plot.plot(pen=device.config_widget.get_color(), name=name)
            self.plot_layouts.append(plot)

    def apply_config(self, name:str):
        device = self.devices.get(name)
        if device:
            device.color = device.config_widget.get_color()
            device.mode = device.config_widget.get_mode()
            device.curve.setPen(device.color)

    def update_data(self):
        for device in self.devices.values():
            device.data = np.roll(device.data, -1)
            mode = device.config_widget.get_mode()
            scale = device.config_widget.get_noise()

            if mode == "Sinus":
                device.step += 1
                device.data[-1] = np.sin(device.step * 0.1)
            elif mode == "Random":
                device.data[-1] = np.random.normal(scale=scale)
            else:
                device.data[-1] = 0

            device.curve.setData(self.x, device.data)

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtWidgets.QApplication(sys.argv)
    win = LivePlotApp()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
