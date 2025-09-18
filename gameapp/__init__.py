from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")  # habilitar CORS para ngrok

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "super-secret-key"  # cámbiala si quieres

    # Inicializar socketio
    socketio.init_app(app)

    # Registrar rutas y sockets
    from gameapp.routes import main_bp
    app.register_blueprint(main_bp)

    import gameapp.sockets  # importa eventos

    return app
