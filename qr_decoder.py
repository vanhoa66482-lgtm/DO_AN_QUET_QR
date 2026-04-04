"""
NHIỆM VỤ CỦA FILE QR_DECODER:
1. Nhận các khung hình (frames) từ camera do ui_manager gửi tới.
2. Sử dụng thư viện pyzbar để tìm kiếm và giải mã (decode) mã QR trong ảnh.
3. Trích xuất dữ liệu thô (chuỗi văn bản/link) từ mã QR.
4. (Nâng cao) Xác định tọa độ khung hình chữ nhật của mã QR để vẽ vòng bao 
   lên màn hình, giúp người dùng biết máy đã nhận diện được.
5. Trả kết quả về cho ui_manager hiển thị và data_manager lưu trữ.
"""

"""
Những thư viện cần tham khảo: opencv-python (cv2), pyzbar, ...
"""