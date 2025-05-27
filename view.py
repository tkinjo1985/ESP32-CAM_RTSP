import cv2
import sys
from typing import Tuple

# 定数定義
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
ESP_IP = "192.168.0.100"
RTSP_URL = f"rtsp://{ESP_IP}:8554/mjpeg/1"
BLUE = (255, 0, 0)
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5

def init_cascade() -> cv2.CascadeClassifier:
    cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if cascade.empty():
        print("Error: カスケード分類器の読み込みに失敗しました")
        sys.exit(1)
    return cascade

def process_frame(frame: cv2.Mat, cascade: cv2.CascadeClassifier) -> Tuple[cv2.Mat, bool]:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS)
    
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), BLUE, 2)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    return frame, key == ord("q")

def main():
    face_cascade = init_cascade()
    vcap = cv2.VideoCapture(RTSP_URL)
    
    if not vcap.isOpened():
        print("Error: RTSPストリームに接続できません")
        sys.exit(1)

    try:
        while True:
            ret, frame = vcap.read()
            if not ret:
                print("Error: フレームの取得に失敗しました")
                break
            
            _, should_exit = process_frame(frame, face_cascade)
            if should_exit:
                break
                
    finally:
        vcap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
