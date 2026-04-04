"""
NHIỆM VỤ CỦA FILE MAIN:
1. Là điểm khởi đầu (Entry Point) duy nhất của toàn bộ ứng dụng.
2. Kết nối và điều phối 3 "chi nhánh": ui_manager, qr_decoder, và data_manager.
3. Khởi tạo cửa sổ chính và kích hoạt vòng lặp chạy ứng dụng (mainloop).
4. Đảm bảo các thành phần phối hợp nhịp nhàng: 
   - UI nhận lệnh quét -> Decoder xử lý -> UI hiện kết quả -> Data lưu vào log.
"""

"""
Các module nội bộ cần kết nối: ui_manager, qr_decoder, data_manager
"""

print("Hello anh em, day la source code!")