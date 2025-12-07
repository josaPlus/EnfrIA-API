from flask import Blueprint, jsonify
from src.services.analysis_service import run_full_analysis
from src.models.app_state import global_state

# Creamos el Blueprint para las rutas API
api_bp = Blueprint('api', __name__)

@api_bp.route('/sensor_abierto', methods=['GET'])
def sensor_trigger():
    print("\nSensor activado: Iniciando análisis...")
    
    resultado = run_full_analysis()
    
    # Actualizamos el estado global
    global_state.update_scan(resultado)
    
    print(f"Análisis finalizado. Total: {resultado.get('total_alimentos', 0)}")
    return jsonify(resultado)

@api_bp.route('/obtener_estado', methods=['GET'])
def get_status():
    return jsonify(global_state.get_state())