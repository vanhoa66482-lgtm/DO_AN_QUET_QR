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

"""
Module: qr_decoder.py
Chức năng: Quản lý Camera, nhận diện, giải mã QR bằng AI (QReader).
Người phụ trách: Nguyễn Lê Phúc Thịnh
"""

import time
from typing import Tuple, Optional
import cv2
from qreader import QReader


class QRDecoder:
    def __init__(self, camera_index: int = 0):
        self.cap = cv2.VideoCapture(camera_index)
        self.scanned_history = {}
        self.cooldown_time = 3.0
        
        print("Đang khởi động AI QReader... (Lần đầu sẽ mất khoảng 5-10 giây để tải mô hình)")
        # Khởi tạo bộ não AI
        self.qreader = QReader()
        print("Tải AI thành công! Sẵn sàng quét mã nghệ thuật.")

    def _classify_data(self, content: str) -> str:
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
        success, frame = self.cap.read()
        if not success:
            return None, None, None

        qr_data_result = None
        qr_type_result = None

        # Đổi sang RGB NGAY TỪ ĐẦU (Vì QReader yêu cầu ảnh RGB để AI nhìn màu cho chuẩn)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # AI BẮT ĐẦU TÌM KIẾM VÀ GIẢI MÁ
        # return_detections=True để AI trả về cả tọa độ vẽ khung
        decoded_texts, detections = self.qreader.detect_and_decode(image=frame_rgb, return_detections=True)

        # Nếu AI tìm thấy mã
        if decoded_texts:
            for i in range(len(decoded_texts)):
                qr_data = decoded_texts[i]
                
                # Bỏ qua nếu AI tìm thấy khung nhưng mã nát đến mức không thể dịch được chữ nào
                if qr_data is None: 
                    continue
                
                # VẼ KHUNG XANH NHẬN DIỆN
                bbox = detections[i]['bbox_xyxy'] # Lấy tọa độ
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 255, 0), 3) # Màu RGB: Xanh lá
                
                display_text = qr_data if len(qr_data) < 25 else qr_data[:25] + "..."
                cv2.putText(frame_rgb, display_text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2) # Màu RGB: Đỏ

                # THUẬT TOÁN COOLDOWN
                current_time = time.time()
                last_scan_time = self.scanned_history.get(qr_data, 0)

                if (current_time - last_scan_time) > self.cooldown_time:
                    self.scanned_history[qr_data] = current_time
                    qr_data_result = qr_data
                    qr_type_result = self._classify_data(qr_data)

        # Trả thẳng ảnh RGB về cho UI hiển thị
        return frame_rgb, qr_data_result, qr_type_result

    def release_camera(self):
        if self.cap.isOpened():
            self.cap.release()

# ========================================================
# PHẦN TEST ĐỘC LẬP
# ========================================================
if __name__ == "__main__":
    may_quet_test = QRDecoder()
    
    while True:
        anh_rgb, noi_dung, phan_loai = may_quet_test.get_frame_and_data()

        if noi_dung is not None:
            print(f"\n[BÍP!] AI QUÉT THÀNH CÔNG:")
            print(f"- Nội dung: {noi_dung}")
            print(f"- Phân loại: {phan_loai}")
            print("-" * 30)

        if anh_rgb is not None:
            anh_bgr_de_test = cv2.cvtColor(anh_rgb, cv2.COLOR_RGB2BGR)
            cv2.imshow("Cua so Test - AI QReader", anh_bgr_de_test)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    may_quet_test.release_camera()
    cv2.destroyAllWindows()