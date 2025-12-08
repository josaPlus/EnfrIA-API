import cv2
import os
from datetime import datetime
from config import OUTPUT_DIR

class CropImage:
    def __init__(self, image_path: str):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        self.height, self.width, _ = self.image.shape

    def recortar_alimentos(self, datos_json: list):
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f" directorio creado: {OUTPUT_DIR}")

        rutas_recortes = []
        print("iniciando recortes")
        
        for i, item in enumerate(datos_json):
            label = item["label"]
            box = item["box_2d"]  # [ymin, xmin, ymax, xmax] en escala 0-1000

            # Convertir coordenadas de escala 1000 a píxeles reales
            ymin = int((box[0] / 1000) * self.height)
            xmin = int((box[1] / 1000) * self.width)
            ymax = int((box[2] / 1000) * self.height)
            xmax = int((box[3] / 1000) * self.width)

            # Asegurar que las coordenadas estén dentro de la imagen
            xmin = max(0, xmin)
            ymin = max(0, ymin)
            xmax = min(self.width, xmax)
            ymax = min(self.height, ymax)

            # Recortar imagen
            recorte = self.image[ymin:ymax, xmin:xmax]

            # Verificar que el recorte tenga tamaño válido
            if recorte.size == 0:
                print(f"Recorte vacío para '{label}'. Saltando.")
                continue

            # Generar nombre de archivo seguro
            label_seguro = label.replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            nombre_archivo = f"{OUTPUT_DIR}/{i}_{label_seguro}_{timestamp}.jpg"

            # Guardar el recorte
            cv2.imwrite(nombre_archivo, recorte)
            rutas_recortes.append(nombre_archivo)
            print(f"guardado: {nombre_archivo} ({recorte.shape[1]}x{recorte.shape[0]})")
            
        print(f"\nrecortes completados: {len(rutas_recortes)} imágenes guardadas")
        return rutas_recortes

def limpiar_archivos(temp_image, recortes):
    try:
        if os.path.exists(temp_image): 
            os.remove(temp_image)
        
        if recortes:
            for recorte in recortes:
                if os.path.exists(recorte):
                    os.remove(recorte)
                    
        print("Archivos temporales limpiados correctamente.")
        
    except Exception as e:
        print(f"Error limpiando: {e}")