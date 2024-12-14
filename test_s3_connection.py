import boto3
import os
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()

print("AWS_ACCESS_KEY:", os.getenv('AWS_ACCESS_KEY'))
print("AWS_SECRET_KEY:", os.getenv('AWS_SECRET_KEY'))
print("AWS_REGION:", os.getenv('AWS_REGION'))

def test_s3_connection():
    try:
        # Crear cliente S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        # Listar buckets como prueba
        response = s3.list_buckets()
        print("Conexión exitosa. Buckets disponibles:")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Error al conectar con S3: {e}")

test_s3_connection()
