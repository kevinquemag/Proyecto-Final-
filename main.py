from app import create_app, db
from app.models import Meme
from dotenv import load_dotenv  # Importa load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()
app = create_app()

with app.app_context():
    memes = Meme.query.all()
    print("Memes en la base de datos:")
    for meme in memes:
        print(f"ID: {meme.id}, Descripción: {meme.descripcion}, Ruta: {meme.ruta}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
