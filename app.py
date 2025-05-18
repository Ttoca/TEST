from flask import Flask
from flask_cors import CORS
from api.auth import auth_bp
from api.empresa import empresa_bp
from api.cola import cola_bp
from Cola_utils import load_colas, save_colas
from api.cola_config import cola_config_bp
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://www.ttoca.online/"}}) 

# Registrar el blueprint de autenticación
app.register_blueprint(auth_bp, url_prefix='/api/auth')

#registro para commitear empresas desde /home
app.register_blueprint(empresa_bp, url_prefix='/api')

#Registro para commitear turnos desde /Dashboard
app.register_blueprint(cola_bp, url_prefix='/api')

#Registro para commitear configuraciones de las distintas queue que puede crear el usuario
app.register_blueprint(cola_config_bp, url_prefix='/api')

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
