import cv2

# OpenCVのデフォルトカスケードパスを利用
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

esp_ip = "192.168.0.100"
vcap = cv2.VideoCapture(f"rtsp://{esp_ip}:8554/mjpeg/1")

try:
    while True:
        ret, frame = vcap.read()
        if not ret:
            print("Failed to acquire frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    vcap.release()
    cv2.destroyAllWindows()
