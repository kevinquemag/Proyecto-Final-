from flask import Blueprint, render_template, request, redirect, url_for, flash
from .utils import upload_to_s3, obtener_etiquetas_immaga, save_meme_to_db, search_memes_in_db
from .models import Meme, Etiqueta

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        usuario = request.form['usuario']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        etiquetas_personalizadas = request.form.get('etiquetas', '')

        if imagen:
            # Subir la imagen a S3
            ruta_imagen = upload_to_s3(imagen)
            if not ruta_imagen:
                flash("Error al subir la imagen", "danger")
                return redirect(url_for('routes.home'))

            # Obtener etiquetas automáticas de Imagga
            etiquetas_automaticas = obtener_etiquetas_immaga(ruta_imagen)

            # Combinar etiquetas
            etiquetas = etiquetas_personalizadas.split(',') + etiquetas_automaticas

            # Guardar meme en la base de datos
            save_meme_to_db(usuario, descripcion, ruta_imagen, etiquetas)
            flash("Meme subido exitosamente", "success")
            return redirect(url_for('routes.home'))

    return render_template('upload.html')

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    resultados = search_memes_in_db(query)
    return render_template('search.html', resultados=resultados)
