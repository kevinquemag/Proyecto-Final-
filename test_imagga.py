from app.utils import obtener_etiquetas_immaga

# URL de prueba de la imagen subida a S3
image_url = "https://cloud-memedb.s3.us-east-2.amazonaws.com/memes/467299285_542809925382136_6184084471025630136_n.jpg"

etiquetas = obtener_etiquetas_immaga(image_url)
print(f"Etiquetas obtenidas: {etiquetas}")
