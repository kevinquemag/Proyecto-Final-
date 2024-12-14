from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    # Cargar variables de entorno
    load_dotenv()

    # Crear la instancia de Flask
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}'
    f'@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
    )


    # Inicializar extensiones
    db.init_app(app)

    # Registrar rutas
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
