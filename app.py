from flask import Flask, send_from_directory, request
from flask_cors import CORS
from api.auth import auth_bp
from api.empresa import empresa_bp
from api.cola import cola_bp
from Cola_utils import load_colas
from api.cola_config import cola_config_bp
import os

# Inicializar Flask
app = Flask(__name__, static_folder='dist')

# CORS
cors_origins = [
    "http://localhost:5173",
    "https://www.ttoca.online/",
]

CORS(app, resources={r"/api/*": {"origins": cors_origins}})

# Cargar colas
load_colas()

# Registrar blueprints de API
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(empresa_bp, url_prefix='/api')
app.register_blueprint(cola_bp, url_prefix='/api')
app.register_blueprint(cola_config_bp, url_prefix='/api')

# Servir archivos estáticos reales
@app.route('/<path:path>')
def serve_static_or_index(path):
    full_path = os.path.join(app.static_folder, path)
    if os.path.isfile(full_path):
        return send_from_directory(app.static_folder, path)
    # Todo lo demás lo maneja React (SPA)
    return send_from_directory(app.static_folder, 'index.html')

# Ruta raíz
@app.route('/')
def serve_root():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
