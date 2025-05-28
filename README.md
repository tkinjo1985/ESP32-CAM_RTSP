# ESP32CAM_RTSP

A network camera project using ESP32-CAM and RTSP protocol with Python-based video processing capabilities.

## Features
- Real-time video streaming using RTSP protocol
- Video reception and processing with Python
- Face detection using OpenCV

## Requirements
### Hardware
- ESP32-CAM
- USB-TTL Serial converter

### Software
- Arduino IDE 2.0 or later
- Python 3.8 or later
- OpenCV 4.0 or later

## Setup
1. ESP32-CAM Configuration
   ```cpp
   // Configure WiFi settings in wifi_config.h
   const char* ssid = "Your_SSID";
   const char* password = "Your_Password";
   ```

2. Programming ESP32-CAM
   - Open esp32_rtsp.ino in Arduino IDE
   - Set board to "AI Thinker ESP32-CAM"
   - Connect ESP32-CAM in programming mode
   - Upload the sketch

3. Python Environment Setup
   ```bash
   pip install opencv-python
   ```

## Usage
1. Power up ESP32-CAM
2. Check IP address in Serial Monitor
3. Configure RTSP URL in Python script
   ```python
   RTSP_URL = f"rtsp://{ESP_IP}:8554/mjpeg/1"
   ```
4. Run Python script
   ```bash
   python view.py
   ```

## Troubleshooting
- Camera initialization error
  - Press reset button on ESP32-CAM
- Connection error
  - Verify WiFi settings and IP address

## License
MIT License

## Contributing
Issues and Pull Requests are welcome.
