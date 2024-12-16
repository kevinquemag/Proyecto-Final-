import boto3
import requests
from werkzeug.utils import secure_filename
import os
from .models import db, Meme, Etiqueta

# Subir imagen a S3
def upload_to_s3(file):
    try:
        filename = secure_filename(file.filename)
        bucket_name = os.getenv('AWS_BUCKET')
        file_path = f"memes/{filename}"

        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        s3_client.upload_fileobj(file, bucket_name, file_path, ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type})
        return f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_path}"
    except Exception as e:
        print(f"Error al subir a S3: {e}")
        return None

def obtener_etiquetas_immaga(image_url):
    api_url = os.getenv('IMAGGA_ENDPOINT', 'https://api.imagga.com/v2/tags')
    auth = (os.getenv('IMAGGA_API_KEY'), os.getenv('IMAGGA_API_SECRET'))
    try:
        print(f"Enviando imagen a Imagga: {image_url}")
        response = requests.get(api_url, auth=auth, params={'image_url': image_url})

        if response.status_code == 200:
            etiquetas = [
                tag['tag']['en']
                for tag in response.json().get('result', {}).get('tags', [])
            ]
            print(f"Respuesta de Imagga: {response.json()}")
            return etiquetas
        else:
            print(f"Error en Imagga: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        print(f"Error al conectar con Imagga: {e}")
        return []


def save_meme_to_db(usuario, descripcion, ruta, etiquetas):
    try:
        # Crear el registro del meme
        meme = Meme(usuario=usuario, descripcion=descripcion, ruta=ruta)
        db.session.add(meme)
        db.session.commit()  # Guarda el meme en la base de datos
        print(f"Meme guardado en la base de datos: {meme.id}")

        # Crear las etiquetas asociadas al meme
        for etiqueta in etiquetas:
            etiqueta_obj = Etiqueta(meme_id=meme.id, etiqueta=etiqueta.strip(), confianza=0.95)
            db.session.add(etiqueta_obj)
        db.session.commit()  # Guarda las etiquetas
        print(f"Etiquetas guardadas: {etiquetas}")

    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

def search_memes_in_db(query):
    try:
        # Buscar memes por descripción
        memes_por_descripcion = Meme.query.filter(Meme.descripcion.like(f"%{query}%")).all()

        # Buscar etiquetas relacionadas
        etiquetas = Etiqueta.query.filter(Etiqueta.etiqueta.like(f"%{query}%")).all()
        meme_ids = [etiqueta.meme_id for etiqueta in etiquetas]

        # Buscar memes asociados a esas etiquetas
        memes_por_etiquetas = Meme.query.filter(Meme.id.in_(meme_ids)).all()

        # Combinar resultados y eliminar duplicados
        return list(set(memes_por_descripcion + memes_por_etiquetas))
    except Exception as e:
        print(f"Error al buscar memes: {e}")
        return []
