"""
NHIỆM VỤ CỦA FILE QR_DECODER:
2. Sử dụng thư viện pyzbar để tìm kiếm và giải mã (decode) mã QR trong ảnh.
3. Trích xuất dữ liệu thô (chuỗi văn bản/link) từ mã QR.
4. (Nâng cao) Xác định tọa độ khung hình chữ nhật của mã QR để vẽ vòng bao 
   lên màn hình, giúp người dùng biết máy đã nhận diện được.
5. Trả kết quả về cho ui_manager hiển thị và data_manager lưu trữ.
"""

"""
Những thư viện cần tham khảo: opencv-python (cv2), pyzbar, ...
"""

"""
Module: qr_decoder.py
Chức năng: Quản lý Camera, nhận diện, giải mã QR và phân loại dữ liệu.
Người phụ trách: Nguyễn Lê Phúc Thịnh
"""

import time
from typing import Tuple, Optional
import cv2
from pyzbar.pyzbar import decode


class QRDecoder:
    """
    Lớp xử lý luồng video từ Camera và giải mã QR.
    Được thiết kế để file ui_manager có thể gọi liên tục mà không gây đơ máy.
    """

    def __init__(self, camera_index: int = 0):
        """
        Khởi tạo kết nối với Camera.
        :param camera_index: ID của camera (mặc định là 0 cho Webcam tích hợp).
        """
        self.cap = cv2.VideoCapture(camera_index)
        
        # Từ điển lưu lịch sử quét để chống spam (Lưu dạng: {nội_dung: thời_gian_quét})
        self.scanned_history = {}
        
        # Thời gian chờ (cooldown) để quét lại cùng một mã (tính bằng giây)
        self.cooldown_time = 3.0

    def _classify_data(self, content: str) -> str:
        """
        [Hàm nội bộ] Phân loại nội dung mã QR.
        :param content: Chuỗi dữ liệu thô giải mã được.
        :return: Loại dữ liệu (Website, WiFi, Liên hệ, hoặc Văn bản).
        """
        content_upper = content.upper()
        if content_upper.startswith(("HTTP://", "HTTPS://", "WWW.")):
            return "Website"
        elif content_upper.startswith("WIFI:"):
            return "WiFi"
        elif content_upper.startswith("BEGIN:VCARD"):
            return "Liên hệ"
        else:
            return "Văn bản"

    def get_frame_and_data(self) -> Tuple[Optional[object], Optional[str], Optional[str]]:
        """
        Đọc một khung hình, giải mã QR (nếu có), vẽ khung nhận diện.
        :return: Tuple gồm (Ảnh_RGB, Nội_dung_QR, Loại_mã). 
                 Nếu không có QR mới, Nội_dung và Loại_mã sẽ trả về None.
        """
        success, frame = self.cap.read()
        if not success:
            return None, None, None

        # Khởi tạo giá trị trả về mặc định
        qr_data_result = None
        qr_type_result = None

        # Đưa khung hình vào pyzbar để giải mã
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            # Giải mã bytes sang string (hỗ trợ tiếng Việt utf-8)
            qr_data = obj.data.decode('utf-8')
            qr_format = obj.type  # QRCODE, BARCODE...
            
            # Lấy tọa độ để vẽ khung
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cắt ngắn text hiển thị trên màn hình nếu nó quá dài
            display_text = qr_data if len(qr_data) < 25 else qr_data[:25] + "..."
            cv2.putText(frame, display_text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # --- THUẬT TOÁN CHỐNG SPAM (COOLDOWN) ---
            if qr_format == 'QRCODE':
                current_time = time.time()
                last_scan_time = self.scanned_history.get(qr_data, 0)

                # Chỉ nhận diện nếu mã này chưa từng quét, hoặc đã cách đây 3 giây
                if (current_time - last_scan_time) > self.cooldown_time:
                    self.scanned_history[qr_data] = current_time
                    qr_data_result = qr_data
                    qr_type_result = self._classify_data(qr_data)

        # Đổi hệ màu từ BGR (OpenCV) sang RGB (chuẩn của Giao diện)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame_rgb, qr_data_result, qr_type_result

    def release_camera(self):
        """
        Giải phóng phần cứng Camera khi tắt ứng dụng.
        Hàm này bắt buộc phải gọi để tránh lỗi "Camera đang được sử dụng" ở lần mở sau.
        """
        if self.cap.isOpened():
            self.cap.release()

# ========================================================
# PHẦN TEST ĐỘC LẬP (Chỉ chạy khi mở trực tiếp file này)
# ========================================================
if __name__ == "__main__":
    print("Đang khởi động Camera để test... (Bấm 'q' để thoát)")
    
    # 1. Tạo ra một cái máy quét
    may_quet_test = QRDecoder()

    while True:
        # 2. Gọi hàm lấy ảnh và dữ liệu
        anh_rgb, noi_dung, phan_loai = may_quet_test.get_frame_and_data()

        # 3. Hiển thị thông tin nếu quét được mã
        if noi_dung is not None:
            print(f"\n[BÍP!] Quét thành công:")
            print(f"- Nội dung: {noi_dung}")
            print(f"- Phân loại: {phan_loai}")
            print("-" * 30)

        # 4. Hiển thị khung hình lên cửa sổ test
        if anh_rgb is not None:
            # LƯU Ý: Vì hàm get_frame_and_data đã đổi ảnh sang RGB cho UI xài
            # Nên để hiển thị bằng cv2.imshow (chuẩn BGR), ta phải đổi ngược lại
            # Nếu không đổi ngược lại, mặt bạn trên camera test sẽ bị màu xanh giống Avatar!
            anh_bgr_de_test = cv2.cvtColor(anh_rgb, cv2.COLOR_RGB2BGR)
            
            cv2.imshow("Cua so Test - QR Decoder", anh_bgr_de_test)

        # 5. Lắng nghe nút 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Đã bấm Q. Đang tắt camera...")
            break

    # 6. Dọn dẹp
    may_quet_test.release_camera()
    cv2.destroyAllWindows()
    print("Đã thoát an toàn!")