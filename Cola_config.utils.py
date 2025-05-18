import json
import os

config_path = "cola_config.json"
if not os.path.exists(config_path):
    with open(config_path, "w") as f:
        json.dump({}, f)

def cargar_configuracion():
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_configuracion(data):
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def obtener_configuracion(empresa_id):
    data = cargar_configuracion()
    return data.get(empresa_id, {})

def guardar_configuracion_empresa(empresa_id, config):
    data = cargar_configuracion()
    data[empresa_id] = config
    guardar_configuracion(data)
