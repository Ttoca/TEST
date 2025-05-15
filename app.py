from flask import Flask, send_from_directory
from flask_cors import CORS
from api.auth import auth_bp
import os

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registrar blueprint de API
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Ruta principal
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Manejador de errores 404 para rutas no encontradas
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
