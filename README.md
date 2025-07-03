---

# 🖱️ Auto Clicker

- **Tác giả:** hadesoverflow
- **Ngôn ngữ:** Python + PyQt5
- **Mục đích:** Tự động click chuột tại nhiều vị trí với các tùy chọn linh hoạt

# 📚 Thư viện đã dùng trong Project: 
- `pip install pyautogui`
- `pip install pyqt5 pyautogui`
- `pip install keyboard`
- `pip install pygetwindow`
- `pip install pywinauto`

## 🔧 Tính năng

* **Click nhiều vị trí:** Ghi nhận 1–10 điểm trên màn hình để click tự động.
* **Thiết lập linh hoạt:**

  * Delay giữa các click (giây)
  * Loại click: Trái / Phải / Double click
  * Số vòng lặp (0 = vô hạn)
* **Phím tắt tiện lợi:**

  * `X`: Tạm dừng
  * `C`: Tiếp tục
* **Lưu trữ tự động:**

  * `click_positions.json` – lưu vị trí click
  * `log.json` – ghi thời gian và vị trí click
* **Giao diện thân thiện:** Thiết kế với PyQt5, dễ thao tác và tùy chỉnh

## 🖥️ Hướng dẫn sử dụng

1. **Chọn vị trí:**

   * Chọn 1 điểm: tự động ghi nhận sau 3 giây.
   * Chọn nhiều điểm: ghi nhận 1–10 vị trí, mỗi vị trí cách nhau 3 giây.
2. **Thiết lập click:**

   * Nhập delay, chọn loại click và số vòng lặp.
3. **Bắt đầu / Dừng:**

   * Nhấn nút chạy hoặc sử dụng phím tắt `X` và `C`.

## 💾 Log & Dữ liệu

* Tự động lưu file JSON trong thư mục `Log`:

  * `click_positions.json`: Danh sách các vị trí click
  * `log.json`: Ghi lại quá trình click
