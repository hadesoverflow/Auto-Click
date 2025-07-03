import sys
import pyautogui
import threading
import time
import keyboard
import json
import datetime
import socket
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QLineEdit, QMessageBox, QSpinBox, QComboBox, QTextEdit, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon


def resource_path(relative_path):
    """Lấy đường dẫn tệp resource (khi build bằng PyInstaller)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Clicker")
        self.setWindowIcon(QIcon(resource_path("Logo/AutoClicker.ico")))
        self.setFixedSize(380, 560)

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
        self.load_positions()

        keyboard.add_hotkey('x', self.stop_by_key)
        keyboard.add_hotkey('c', self.continue_by_key)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #0f2027, stop:1 #203a43);
                color: #e0e0e0;
                font-size: 13px;
            }
            QPushButton {
                padding: 6px;
                font-size: 13px;
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #21CBF3);
                border: none;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1976D2, stop:1 #00ACC1);
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit, QSpinBox, QComboBox, QTextEdit {
                padding: 5px;
                font-size: 13px;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
            }
        """)

        self.label = QLabel("🎯 Số điểm đã chọn: 0")
        self.label.setAlignment(Qt.AlignCenter)

        btn_row = QHBoxLayout()
        self.single_btn = QPushButton("➕ Chọn 1 vị trí")
        self.single_btn.clicked.connect(self.record_single_position)
        self.multi_btn = QPushButton("📍 Chọn nhiều vị trí")
        self.multi_btn.clicked.connect(self.setup_multi_click)
        btn_row.addWidget(self.single_btn)
        btn_row.addWidget(self.multi_btn)

        self.clear_btn = QPushButton("🗑️ Xóa tất cả vị trí")
        self.clear_btn.clicked.connect(self.clear_positions)

        self.delay_label = QLabel("⏱️ Delay giữa mỗi click (giây)")
        self.delay_input = QLineEdit("0.5")

        self.click_type_label = QLabel("🖱️ Loại click")
        self.click_type_box = QComboBox()
        self.click_type_box.addItems(["Click trái", "Click phải", "Double Click"])

        self.loop_label = QLabel("🔁 Số vòng lặp (0 = vô hạn)")
        self.loop_spin = QSpinBox()
        self.loop_spin.setRange(0, 9999)

        self.start_btn = QPushButton("▶️ Bắt đầu Auto Click")
        self.start_btn.clicked.connect(self.toggle_clicking)

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

        self.setLayout(layout)

    def record_click_position(self):
        self.label.setText(f"🎯 Di chuyển chuột trong 3 giây...")
        self.repaint()
        QTimer.singleShot(3000, self.capture_position)

    def capture_position(self):
        p = pyautogui.position()
        pos = {"x": p.x, "y": p.y}

        full_log = {
            "pos": pos,
            "pc_name": self.hostname,
            "folder_path": os.getcwd(),
            "url": None,
            "time": datetime.datetime.now().isoformat()
        }

        try:
            with open("log.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(full_log, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[ERROR] Ghi log.json thất bại: {e}")

        try:
            self.click_positions.append({"pos": pos})
            self.save_positions()
            self.load_positions()
        except Exception as e:
            print(f"[ERROR] Ghi click_positions.json thất bại: {e}")

        if self.multi_click_mode:
            self.multi_click_count += 1
            self.label.setText(f"🔢 Đã chọn {self.multi_click_count}/{self.multi_click_total} điểm")
            if self.multi_click_count < self.multi_click_total:
                QTimer.singleShot(3000, self.record_click_position)
            else:
                self.multi_click_mode = False

    def record_single_position(self):
        if len(self.click_positions) >= 10:
            QMessageBox.warning(self, "Thông báo", "Bạn đã chọn đủ 10 vị trí!")
            return
        self.multi_click_mode = False
        self.record_click_position()

    def setup_multi_click(self):
        if len(self.click_positions) >= 10:
            QMessageBox.warning(self, "Thông báo", "Bạn đã chọn đủ 10 vị trí!")
            return

        max_points = 10 - len(self.click_positions)
        num, ok = QInputDialog.getInt(self, "Chọn nhiều điểm", f"Bạn muốn chọn bao nhiêu điểm? (1 - {max_points})", 1, 1, max_points)
        if ok:
            self.multi_click_mode = True
            self.multi_click_total = num
            self.multi_click_count = 0
            self.record_click_position()

    def clear_positions(self):
        self.click_positions.clear()
        try:
            with open("click_positions.json", "w") as f:
                json.dump([], f)
        except Exception as e:
            print(f"[ERROR] Xóa click_positions.json thất bại: {e}")
        self.label.setText("Số điểm đã chọn: 0")
        self.preview_text.setPlainText("Danh sách đã được xóa!")

    def save_positions(self):
        try:
            with open("click_positions.json", "w") as f:
                json.dump(self.click_positions, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Ghi click_positions.json thất bại: {e}")

    def load_positions(self):
        try:
            with open("click_positions.json", "r") as f:
                self.click_positions = json.load(f)
                self.label.setText(f"Số điểm đã chọn: {len(self.click_positions)}")
                preview = "Danh sách vị trí đã lưu:\n"
                for i, entry in enumerate(self.click_positions):
                    pos = entry['pos']
                    preview += f"{i+1}. Tọa độ: {pos}\n"
                self.preview_text.setPlainText(preview)
        except Exception as e:
            print(f"[ERROR] Tải click_positions.json thất bại: {e}")
            self.click_positions = []

    def toggle_clicking(self):
        if not self.clicking:
            if not self.click_positions:
                QMessageBox.warning(self, "Cảnh báo", "Hãy chọn ít nhất 1 vị trí trước!")
                return
            self.clicking = True
            self.start_btn.setText("⏹️ Dừng Auto Click")
            self.total_loops = self.loop_spin.value()
            self.current_loop = 0
            self.thread = threading.Thread(target=self.auto_click)
            self.thread.start()
        else:
            self.stop_clicking()

    def auto_click(self):
        try:
            delay = float(self.delay_input.text())
            if delay < 0:
                raise ValueError
        except ValueError:
            self.label.setText("❌ Delay không hợp lệ!")
            self.stop_clicking()
            return

        click_type = self.click_type_box.currentText()

        while self.clicking:
            for entry in self.click_positions:
                pos = entry['pos']
                if not self.clicking:
                    break
                if click_type == "Click trái":
                    pyautogui.click(pos['x'], pos['y'])
                elif click_type == "Click phải":
                    pyautogui.click(pos['x'], pos['y'], button='right')
                elif click_type == "Double Click":
                    pyautogui.doubleClick(pos['x'], pos['y'])
                time.sleep(delay)

            self.current_loop += 1
            if self.total_loops > 0 and self.current_loop >= self.total_loops:
                self.label.setText(f"✅ Đã hoàn tất {self.current_loop} vòng lặp.")
                self.stop_clicking()
                return

    def stop_clicking(self):
        self.clicking = False
        self.start_btn.setText("▶️ Bắt đầu Auto Click")

    def stop_by_key(self):
        if self.clicking:
            self.stop_clicking()
            self.label.setText("⛔ Auto click đã tạm dừng (phím X)")

    def continue_by_key(self):
        if not self.clicking and self.click_positions:
            self.clicking = True
            self.start_btn.setText("⏹️ Dừng Auto Click")
            self.thread = threading.Thread(target=self.auto_click)
            self.thread.start()
            self.label.setText("▶️ Tiếp tục Auto click (phím C)")

    def closeEvent(self, event):
        keyboard.remove_hotkey('x')
        keyboard.remove_hotkey('c')
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    window.show()
    sys.exit(app.exec_())
