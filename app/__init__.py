from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirige a la página de login si no está autenticado
login_manager.login_message = 'Debes iniciar sesión para ver esta página.'
login_manager.login_message_category = 'info'

# Inicializamos el serializador aquí para que esté disponible en toda la app
serializer = None

def create_app():
    global serializer
    app = Flask(__name__, instance_relative_config=True)
    
    # --- Configuración ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
    # Ubicación de la base de datos SQLite dentro de la carpeta 'instance'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializamos el serializador con la secret_key
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # --- Inicializar Extensiones ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # Flask-Login usa esto para recargar el objeto de usuario desde el ID de usuario almacenado en la sesión.
        return User.query.get(int(user_id))

    # --- Registrar Blueprints ---
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app