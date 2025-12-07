import os
from dotenv import load_dotenv
from ultralytics import YOLO

# Cargar las variables del archivo .env
load_dotenv()

# Leer las variables de entorno
CAMERA_URL = os.getenv("CAMERA_URL") 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validar que existan (Buena práctica)
if not GEMINI_API_KEY:
    raise ValueError("ERROR: No se encontró GEMINI_API_KEY en el archivo .env")

# --- Configuraciones normales ---
MODEL_PATH = "runs/healthy-rotten10/weights/best.pt"
OUTPUT_DIR = "recortes_alimentos"

# --- Carga del Modelo ---
print("Cargando configuración y modelo YOLO...")
try:
    YOLO_MODEL = YOLO(MODEL_PATH)
    print("YOLO cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar YOLO: {e}")
    YOLO_MODEL = None