"""
NHIỆM VỤ CỦA FILE DATA_MANAGER:
1. Nhận dữ liệu từ qr_decoder.py sau khi quét thành công.
2. Lấy thời gian hiện tại từ hệ thống.
3. Ghi dữ liệu vào file 'scan_logs.txt' theo định dạng:
    [STT]: Số thứ tự (1, 2, 3...)
    [Thời gian]: Ngày giờ quét (VD: 11/04 10:00)
    [Loại mã]: Phân loại xem nó là cái gì (VD: Website, WiFi, Văn bản, Thẻ liên hệ...)
    [Nội dung]: Cục dữ liệu gốc quét được (VD: https://hcmute.edu.vn)
4. Lưu ý: Dùng chế độ 'a' (append) để không làm mất dữ liệu cũ.
"""
"""
Những thư viện cần tham khảo: datetime, pathlib, csv, ...
"""
import datetime
LOG_FILE_PATH = "scan_logs.txt"
def write_to_scan_logs(qr_content):
    # Bước 1: Lấy thời gian (Day/Month/Year Hour:Minute)
    # Bước 2: Mở file scan_logs.txt (encoding='utf-8')
    # Bước 3: Ghi dòng mới vào cuối file
    pass