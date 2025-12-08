from datetime import datetime

class SystemState:
    def __init__(self):
        self.state = {
            # "mensaje": "Esperando sensor",
            "timestamp": None,
            "scan_id": 0,
            "total_alimentos": 0,
            "alimentos_detectados": []
        }

    def get_state(self):
        return self.state

    def update_scan(self, resultado_analisis):
        if "error" not in resultado_analisis:
            self.state["scan_id"] += 1
            self.state["timestamp"] = datetime.now().isoformat()
            self.state.update(resultado_analisis)
            return True
        return False

# Instancia global única
global_state = SystemState()