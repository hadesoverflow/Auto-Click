# utils.py

import os
import sys
import keyboard

def resource_path(relative_path):
    """Lấy đường dẫn tài nguyên tương thích khi build với PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def setup_hotkeys(self):
    """Thiết lập phím tắt X và C để tạm dừng / tiếp tục AutoClicker."""
    keyboard.add_hotkey('x', lambda: self.stop_by_key())
    keyboard.add_hotkey('c', lambda: self.continue_by_key())

def cleanup_hotkeys():
    """Xoá hotkey khi đóng ứng dụng để tránh treo phím tắt."""
    keyboard.remove_hotkey('x')
    keyboard.remove_hotkey('c')
