from flask import Flask, send_from_directory
from flask_cors import CORS
from api.auth import auth_bp
import os

app = Flask(__name__, static_folder='dist', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registrar blueprint de API
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Fallback para rutas SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    full_path = os.path.join(app.static_folder, path)

    # ✅ Solo servimos el archivo si es un archivo regular (no directorio)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(app.static_folder, path)

    # 🟩 Cualquier otra ruta (como /login, /dashboard) => index.html
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
