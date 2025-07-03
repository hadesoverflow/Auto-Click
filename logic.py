import json
import datetime
import threading
import pyautogui
import os
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QInputDialog

LOG_DIR = os.path.join(os.getcwd(), "log")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "log.json")
CLICK_POSITIONS_PATH = os.path.join(LOG_DIR, "click_positions.json")

def get_stylesheet():
    return """
    QWidget {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #141e30, stop:1 #243b55);
        color: #f0f0f0;
        font-size: 13px;
    }
    QPushButton {
        padding: 6px;
        font-size: 13px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2);
        border: none;
        color: white;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #6a11cb, stop:1 #2575fc);
    }
    QLabel {
        font-weight: bold;
    }
    QLineEdit, QSpinBox, QComboBox, QTextEdit {
        padding: 5px;
        font-size: 13px;
        border-radius: 4px;
        background-color: #1c1c2b;
        color: white;
        border: 1px solid #444;
    }
    QMenuBar {
        background-color: #141e30;
        color: #f0f0f0;
    }
    QMenuBar::item:selected {
        background-color: #203a43;
    }
    QMenu {
        background-color: #1c1c2b;
        color: #f0f0f0;
        border: 1px solid #444;
    }
    QMenu::item:selected {
        background-color: #3e3e5e;
    }
    """
    
def record_click_position(self):
    self.label.setText("🎯 Di chuyển chuột trong 3 giây...")
    self.repaint()
    QTimer.singleShot(3000, lambda: capture_position(self))

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
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(full_log, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[ERROR] Ghi log.json thất bại: {e}")

    try:
        self.click_positions.append({"pos": pos})
        save_positions(self)
        load_positions(self)
    except Exception as e:
        print(f"[ERROR] Ghi click_positions.json thất bại: {e}")

    if self.multi_click_mode:
        self.multi_click_count += 1
        self.label.setText(f"🔢 Đã chọn {self.multi_click_count}/{self.multi_click_total} điểm")
        if self.multi_click_count < self.multi_click_total:
            QTimer.singleShot(3000, lambda: record_click_position(self))
        else:
            self.multi_click_mode = False

def record_single_position(self):
    if len(self.click_positions) >= 10:
        QMessageBox.warning(self, "Thông báo", "Bạn đã chọn đủ 10 vị trí!")
        return
    self.multi_click_mode = False
    record_click_position(self)

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
        record_click_position(self)

def clear_positions(self):
    self.click_positions.clear()
    try:
        with open(CLICK_POSITIONS_PATH, "w") as f:
            json.dump([], f)
    except Exception as e:
        print(f"[ERROR] Xóa click_positions.json thất bại: {e}")
    self.label.setText("Số điểm đã chọn: 0")
    self.preview_text.setPlainText("Danh sách đã được xóa!")

def save_positions(self):
    try:
        with open(CLICK_POSITIONS_PATH, "w") as f:
            json.dump(self.click_positions, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Ghi click_positions.json thất bại: {e}")

def load_positions(self):
    try:
        with open(CLICK_POSITIONS_PATH, "r") as f:
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
        self.thread = threading.Thread(target=lambda: auto_click(self))
        self.thread.start()
    else:
        stop_clicking(self)

def auto_click(self):
    try:
        delay = float(self.delay_input.text())
        if delay < 0:
            raise ValueError
    except ValueError:
        self.label.setText("❌ Delay không hợp lệ!")
        stop_clicking(self)
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
            stop_clicking(self)
            return

def stop_clicking(self):
    self.clicking = False
    self.start_btn.setText("▶️ Bắt đầu Auto Click")

def stop_by_key(self):
    if self.clicking:
        stop_clicking(self)
        self.label.setText("⛔ Auto click đã tạm dừng")

def continue_by_key(self):
    if not self.clicking and self.click_positions:
        self.clicking = True
        self.start_btn.setText("⏹️ Dừng Auto Click")
        self.thread = threading.Thread(target=lambda: auto_click(self))
        self.thread.start()
        self.label.setText("▶️ Tiếp tục Auto click")
