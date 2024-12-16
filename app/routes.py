from flask import Blueprint, request, render_template, redirect, url_for, flash
from .utils import upload_to_s3, obtener_etiquetas_immaga, save_meme_to_db, search_memes_in_db
from app.models import Meme, Etiqueta

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')
        etiquetas_personalizadas = request.form.get('etiquetas', '')

        if imagen:
            # Subir imagen a S3
            ruta_imagen = upload_to_s3(imagen)
            if ruta_imagen:
             
                etiquetas_automaticas = obtener_etiquetas_immaga(ruta_imagen)
                print(f"Etiquetas automáticas obtenidas: {etiquetas_automaticas}")

                # Procesar etiquetas personalizadas ingresadas por el usuario
                etiquetas_personalizadas_lista = [
                    etiqueta.strip() for etiqueta in etiquetas_personalizadas.split(',')
                ] if etiquetas_personalizadas else []
                print(f"Etiquetas personalizadas ingresadas: {etiquetas_personalizadas_lista}")

                # Combinar ambas listas de etiquetas
                etiquetas_combinadas = etiquetas_automaticas + etiquetas_personalizadas_lista
                print(f"Todas las etiquetas combinadas: {etiquetas_combinadas}")

                # Guardar en la base de datos
                save_meme_to_db(usuario, descripcion, ruta_imagen, etiquetas_automaticas)

                flash("Meme subido exitosamente y etiquetas generadas.", "success")
                return redirect(url_for('routes.search'))
            else:
                flash("Error al subir la imagen a S3.", "danger")
    return render_template('upload.html')

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    resultados = []

    if query:
        resultados = search_memes_in_db(query)
    else:
        resultados = Meme.query.all()

    # Recuperar etiquetas asociadas (tanto personalizadas como automáticas)
    resultados_con_etiquetas = []
    for meme in resultados:
        etiquetas = Etiqueta.query.filter_by(meme_id=meme.id).all()
        etiquetas_list = [etiqueta.etiqueta for etiqueta in etiquetas]
        resultados_con_etiquetas.append({
            'meme': meme,
            'etiquetas': etiquetas_list
        })

    return render_template('search.html', resultados=resultados_con_etiquetas)