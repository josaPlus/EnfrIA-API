import cv2
import os
from datetime import datetime
from config import CAMERA_URL

CAPTURE_DIR = "capturas"

def capture_image():
    print(f"📷 Conectando a {CAMERA_URL}...")
    cap = cv2.VideoCapture(CAMERA_URL)
    
    if not cap.isOpened():
        return None, "No se pudo conectar a la cámara"

    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return None, "Frame vacío"

    if not os.path.exists(CAPTURE_DIR):
        os.makedirs(CAPTURE_DIR)
        print(f"Carpeta creada: {CAPTURE_DIR}")

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Guardamos dentro de la carpeta 'capturas'
    temp_path = f"{CAPTURE_DIR}/captura_{timestamp_str}.jpg"
    
    cv2.imwrite(temp_path, frame)
    return temp_path, None