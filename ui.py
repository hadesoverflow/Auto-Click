import sys
import os
import socket
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QSpinBox, QComboBox, QTextEdit, QMenuBar, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from guide import GuideDialog
from logic import *

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class AutoClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Clicker")
        self.setWindowIcon(QIcon(resource_path("resources/AutoClicker.ico")))
        self.setFixedSize(380, 590)

        self.hostname = socket.gethostname()
        self.click_positions = []
        self.clicking = False
        self.thread = None
        self.total_loops = 0
        self.current_loop = 0
        self.multi_click_mode = False
        self.multi_click_total = 0
        self.multi_click_count = 0

        self.init_ui()
        load_positions(self)
        self.bind_hotkeys()

    def init_ui(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Trợ giúp")
        guide_action = QAction("Hướng dẫn sử dụng", self)
        guide_action.triggered.connect(self.show_guide)
        help_menu.addAction(guide_action)

        layout = QVBoxLayout()
        self.setStyleSheet(get_stylesheet())

        self.label = QLabel("🎯 Số điểm đã chọn: 0")
        self.label.setAlignment(Qt.AlignCenter)

        btn_row = QHBoxLayout()
        self.single_btn = QPushButton("➕ Chọn 1 vị trí")
        self.single_btn.clicked.connect(lambda: record_single_position(self))
        self.multi_btn = QPushButton("📍 Chọn nhiều vị trí")
        self.multi_btn.clicked.connect(lambda: setup_multi_click(self))
        btn_row.addWidget(self.single_btn)
        btn_row.addWidget(self.multi_btn)

        self.clear_btn = QPushButton("🗑️ Xóa tất cả vị trí")
        self.clear_btn.clicked.connect(lambda: clear_positions(self))

        self.delay_label = QLabel("⏱️ Delay giữa mỗi click (giây)")
        self.delay_input = QLineEdit("0.5")

        self.click_type_label = QLabel("🖱️ Loại click")
        self.click_type_box = QComboBox()
        self.click_type_box.addItems(["Click trái", "Click phải", "Double Click"])

        self.loop_label = QLabel("🔁 Số vòng lặp (0 = vô hạn)")
        self.loop_spin = QSpinBox()
        self.loop_spin.setRange(0, 9999)

        self.start_btn = QPushButton("▶️ Bắt đầu Auto Click")
        self.start_btn.clicked.connect(lambda: toggle_clicking(self))

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFixedHeight(140)
        self.preview_text.setStyleSheet("background-color: #121212; color: #00ff00;")
        self.preview_text.setPlaceholderText("Vị trí auto click sẽ hiển thị tại đây...")

        credit = QLabel("<i class='fa fa-cloud'></i> Created by hadesoverflow")
        credit.setAlignment(Qt.AlignCenter)
        credit.setTextFormat(Qt.RichText)
        credit.setStyleSheet("color: gray; font-style: italic; padding-top: 8px;")

        layout.addWidget(self.label)
        layout.addLayout(btn_row)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_input)
        layout.addWidget(self.click_type_label)
        layout.addWidget(self.click_type_box)
        layout.addWidget(self.loop_label)
        layout.addWidget(self.loop_spin)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.preview_text)
        layout.addWidget(credit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def bind_hotkeys(self):
        import keyboard
        keyboard.add_hotkey('x', lambda: stop_by_key(self))
        keyboard.add_hotkey('c', lambda: continue_by_key(self))

    def show_guide(self):
        dialog = GuideDialog(self)
        dialog.exec_()

    def closeEvent(self, event):
        import keyboard
        keyboard.remove_hotkey('x')
        keyboard.remove_hotkey('c')
        event.accept()
