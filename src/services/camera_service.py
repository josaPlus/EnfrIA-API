import cv2
from datetime import datetime
from config import CAMERA_URL

def capture_image():
    print(f"📷 Conectando a {CAMERA_URL}...")
    cap = cv2.VideoCapture(CAMERA_URL)
    
    if not cap.isOpened():
        return None, "No se pudo conectar a la cámara"

    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return None, "Frame vacío"

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"captura_{timestamp_str}.jpg"
    cv2.imwrite(temp_path, frame)
    return temp_path, None