from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import Qt

class GuideDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hướng dẫn sử dụng")
        self.setFixedSize(600, 650)

        self.setStyleSheet("""
            QDialog {
                background-color: #141e30;  /* Nền xanh đậm */
                color: #f0f0f0;
                font-size: 13px;
            }
            QTextEdit {
                background-color: #1c1c2b;
                color: white;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
            }
            QLabel {
                font-weight: bold;
                font-size: 15px;
                margin-bottom: 8px;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("📘 Auto Clicker - Hướng dẫn sử dụng")
        title.setAlignment(Qt.AlignCenter)

        guide_text = QTextEdit()
        guide_text.setReadOnly(True)
        guide_text.setText("""
Ứng dụng này giúp bạn tự động click chuột tại nhiều vị trí với các lựa chọn về số lần lặp, loại click và delay giữa mỗi click.

1. Giao diện chính
- Chọn 1 vị trí: Ghi nhận 1 điểm sau 3 giây.
- Chọn nhiều vị trí: Chọn 1–10 điểm, mỗi điểm sau 3 giây.
- Xóa tất cả vị trí: Xóa danh sách điểm đã lưu.

2. Thiết lập
- Delay (giây): Thời gian giữa mỗi click.
- Loại click: Trái / Phải / Double click.
- Số vòng lặp: 0 là vô hạn.

3. Phím tắt
- X: Tạm dừng
- C: Tiếp tục

4. Lưu trữ
- Log: Lưu vị trí và thời gian
- Tự động lưu click_positions.json và log.json trong thư mục Log

Tác giả: hadesoverflow
        """)

        layout.addWidget(title)
        layout.addWidget(guide_text)
        self.setLayout(layout)
