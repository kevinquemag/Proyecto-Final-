import boto3
import requests
import os
from werkzeug.utils import secure_filename
from .models import db, Meme, Etiqueta

# Subir imagen a S3
def upload_to_s3(file):
    # Crear el cliente de S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    try:
        # Asegurar un nombre seguro para el archivo
        filename = secure_filename(file.filename)
        bucket_name = os.getenv('AWS_BUCKET_NAME').replace(' ', '%20')  # Manejar espacios
        file_path = f"memes/{filename}"  # Ruta dentro del bucket

        # Subir el archivo al bucket S3
        s3_client.upload_fileobj(
            file,
            bucket_name.replace('%20', ' '),  # Revertir espacio codificado para la API
            file_path,
            ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type}
        )

        # Construir la URL pública de la imagen
        region = os.getenv('AWS_REGION')
        return f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_path}".replace(' ', '%20')
    except Exception as e:
        print(f"Error al subir a S3: {e}")
        return None

# Etiquetas automáticas con Imagga
def obtener_etiquetas_immaga(image_url):
    api_url = os.getenv('IMAGGA_ENDPOINT', 'https://api.imagga.com/v2/tags')
    auth = (os.getenv('IMAGGA_API_KEY'), os.getenv('IMAGGA_API_SECRET'))
    try:
        response = requests.get(api_url, auth=auth, params={'image_url': image_url})
        if response.status_code == 200:
            return [tag['tag']['en'] for tag in response.json().get('result', {}).get('tags', [])]
        else:
            print(f"Error en Imagga: {response.text}")
            return []
    except Exception as e:
        print(f"Error al conectar con Imagga: {e}")
        return []

# Guardar meme en la base de datos
def save_meme_to_db(usuario, descripcion, ruta, etiquetas):
    meme = Meme(usuario=usuario, descripcion=descripcion, ruta=ruta)
    db.session.add(meme)
    db.session.commit()

    for etiqueta in etiquetas:
        etiqueta_obj = Etiqueta(meme_id=meme.id, etiqueta=etiqueta, confianza=0.95)
        db.session.add(etiqueta_obj)
    db.session.commit()

def search_memes_in_db(query):
    """
    Busca memes en la base de datos por descripción o etiquetas.
    Args:
        query (str): Palabra clave para buscar memes.
    Returns:
        list: Lista de objetos Meme encontrados.
    """
    try:
        # Busca memes que coincidan con la descripción
        memes_por_descripcion = Meme.query.filter(Meme.descripcion.like(f"%{query}%")).all()

        # Busca etiquetas que coincidan con la consulta
        etiquetas = Etiqueta.query.filter(Etiqueta.etiqueta.like(f"%{query}%")).all()
        meme_ids = [etiqueta.meme_id for etiqueta in etiquetas]

        # Busca memes asociados con esas etiquetas
        memes_por_etiquetas = Meme.query.filter(Meme.id.in_(meme_ids)).all()

        # Combina y elimina duplicados
        return list(set(memes_por_descripcion + memes_por_etiquetas))
    except Exception as e:
        print(f"Error al buscar memes: {e}")
        return []
