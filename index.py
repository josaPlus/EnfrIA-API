from flask import Flask
from src.routers.api_routes import api_bp

app = Flask(__name__)

# Registrar el blueprint (conectar las rutas)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    print("Iniciando API RefriA...")
    # Puedes configurar host y puerto aquí
    app.run(host='0.0.0.0', port=5000, debug=True)