# EnfrIA API: Backend para Refrigerador Inteligente 🍎🥦



API RESTful desarrollada en Flask que actúa como el "cerebro" del sistema de refrigerador inteligente **EnfrIA**. Este backend orquesta la captura de imágenes, la detección de objetos con Inteligencia Artificial Generativa (Gemini) y la clasificación de estado con Visión Computacional (YOLO).

Diseñada para interactuar con un microcontrolador **ESP32** (sensor/cámara) y una aplicación móvil **Jetpack Compose**.

## 👥 Integrantes

* Josafat Aguirre
* Ruth Manríquez
* Camila Liedo
* Mariana Ortiz
* Andrés Aguilera

## 📝 Descripción del Flujo

El sistema funciona mediante un pipeline de procesamiento secuencial:

1.  **Trigger IoT:** El ESP32 detecta que la puerta del refrigerador se ha cerrado y envía una señal al endpoint `/sensor_abierto`.
2.  **Captura:** La API se conecta a la cámara IP y descarga el frame actual.
3.  **Detección Semántica (Gemini AI):** Se envía la imagen a Google Gemini 2.5 Flash Lite para identificar *qué* alimentos hay y obtener sus coordenadas.
4.  **Procesamiento:** El sistema recorta cada alimento detectado en imágenes individuales.
5.  **Clasificación de Estado (YOLOv8):** Cada recorte pasa por una red neuronal convolucional entrenada para determinar si el alimento está **FRESCO** o **PODRIDO**.
6.  **Respuesta:** Se devuelve un JSON con el inventario actualizado y se guarda en el estado global para la App Móvil.

## ✨ Características Principales

* ✅ **Arquitectura Modular:** Código organizado profesionalmente en Routers, Services y Models.
* ✅ **IA Híbrida:** Combina la capacidad de entendimiento de Gemini con la velocidad de clasificación de YOLO.
* ✅ **Integración IoT & Móvil:** Endpoints específicos para sensores y para consumo de UI.
* ✅ **Gestión de Estado:** Mantiene un registro en memoria del último análisis para consultas rápidas desde la App.
* ✅ **Seguridad:** Manejo de credenciales sensibles mediante variables de entorno (`.env`).

## 🛠️ Requisitos del Sistema

### Software
* **Python:** 3.10 o superior.
* **Pip:** Gestor de paquetes actualizado.
* **Git:** Para control de versiones.

### Variables de Entorno
Necesitas configurar un archivo `.env` con:
* `GEMINI_API_KEY`: Tu llave de Google AI Studio.
* `CAMERA_URL`: La dirección IP local de tu ESP32-CAM (ej: `http://192.168.1.XX:8080/video`).

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el servidor localmente:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Ace707-dev/enfrIA-api.git](https://github.com/Ace707-dev/enfrIA-api.git)
cd enfrIA-api