import os
import cv2
from config import YOLO_MODEL
from .camera_service import capture_image
from .gemini_service import GeminiAPI
from .image_utils import CropImage, limpiar_archivos

def run_full_analysis():
    if YOLO_MODEL is None:
        return {"error": "YOLO no cargado"}

    # Captura
    temp_path, error = capture_image()
    if error: return {"error": error}

    recortes = []
    try:
        # Gemini
        gemini = GeminiAPI()
        coordenadas = gemini.get_food_coordinates(temp_path)
        
        if not coordenadas:
            return {"error": "No se detectaron alimentos"}

        # Recorte
        cropper = CropImage(temp_path)
        recortes = cropper.recortar_alimentos(coordenadas)

        # Clasificación YOLO
        resultados = []
        for i, recorte_path in enumerate(recortes):
            try:
                img = cv2.imread(recorte_path)
                if img is None: continue

                results = YOLO_MODEL.predict(img, imgsz=224, verbose=False)
                res = results[0]
                
                class_name = res.names[res.probs.top1]
                conf = float(res.probs.top1conf.item())
                estado = "FRESCO" if "healthy" in class_name.lower() else "PODRIDO"
                
                nombre_alimento = coordenadas[i]["label"] if i < len(coordenadas) else "Desconocido"
                
                resultados.append({
                    "alimento": nombre_alimento,
                    "estado": estado,
                    "detalle_yolo": class_name,
                    "confianza": round(conf * 100, 2),
                    "imagen_recorte": os.path.basename(recorte_path)
                })
            except Exception as e:
                print(f"Error clasificando {i}: {e}")

        # Respuesta
        frescos = sum(1 for r in resultados if r["estado"] == "FRESCO")
        podridos = sum(1 for r in resultados if r["estado"] == "PODRIDO")

        return {
            "mensaje": "Análisis completado",
            "total_alimentos": len(resultados),
            "frescos": frescos,
            "podridos": podridos,
            "alimentos_detectados": resultados
        }

    except Exception as e:
        return {"error": str(e)}
    
    # Opcional: Llamar a limpiar_archivos(temp_path, recortes) aquí si quieres borrar inmediato
    # finally:
    #     limpiar_archivos(temp_path, recortes)