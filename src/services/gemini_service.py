import google.generativeai as genai
from google.api_core import exceptions
from PIL import Image
import json
import time
import os
from config import GEMINI_API_KEY

class GeminiAPI:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        if hasattr(genai, 'configure'):
            genai.configure(api_key=self.api_key)
        
    def get_food_coordinates(self, image_path: str, reintentos=3):
        # Prompt optimizado
        prompt_especifico = """
        Detecta todos los alimentos en esta imagen.
        Devuelve una respuesta estrictamente en formato JSON.
        No uses bloques de código markdown, solo el JSON crudo.
        
        El JSON debe ser una lista de objetos con:
        - "label": Nombre del alimento en español.
        - "box_2d": [ymin, xmin, ymax, xmax] coordenadas normalizadas (0-1000).
        """


        nombre_modelo = 'gemini-2.5-flash-lite' 

        for intento in range(reintentos):
            try:
                print(f"intentando conectar con Gemini (intento {intento + 1}/{reintentos})")
                img = Image.open(image_path)
                
                model = genai.GenerativeModel(nombre_modelo)
                
                generation_config = genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )

                response = model.generate_content(
                    [prompt_especifico, img],
                    generation_config=generation_config
                )
                
                if response.text:
                    print("coordenadas recibidas de Gemini")
                    clean_text = response.text.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean_text)
                
            except exceptions.ResourceExhausted:
                print("cuota excedida.")
                time.sleep(10) # Espera obligatoria antes de reintentar
                continue # Vuelve al inicio del loop
                
            except Exception as e:
                print(f"error en Gemini: {e}")
                # Si es otro tipo de error, imprimimos y salimos
                return None
        
        print("se agotaron los reintentos con Gemini.")
        return None