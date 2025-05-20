from flask import Flask, send_from_directory
from flask_cors import CORS
from api.auth import auth_bp
from api.empresa import empresa_bp
from api.cola import cola_bp
from api.cola_config import cola_config_bp
from Cola_utils import load_colas
import os

# Inicializar Flask
app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# Cargar datos iniciales
load_colas()

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(empresa_bp, url_prefix='/api')
app.register_blueprint(cola_bp, url_prefix='/api')
app.register_blueprint(cola_config_bp, url_prefix='/api')

# Ruta para servir SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_spa(path):
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
