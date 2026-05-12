import boto3
from datetime import datetime

REGION = "us-east-1"
BUCKET_NAME = "devops-bucket-189399646295"
LOCAL_FILE = "archivo_prueba_s3.txt"
S3_KEY = "pruebas/archivo_prueba_s3.txt"

s3 = boto3.client("s3", region_name=REGION)

with open(LOCAL_FILE, "w", encoding="utf-8") as file:
    file.write("Archivo de prueba para automatización S3 con boto3.\n")
    file.write(f"Fecha de creación: {datetime.now()}\n")

print(f"Archivo local creado: {LOCAL_FILE}")

s3.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)

print(f"Archivo subido a S3: s3://{BUCKET_NAME}/{S3_KEY}")

response = s3.list_objects_v2(Bucket=BUCKET_NAME)

print("\nObjetos encontrados en el bucket:")
if "Contents" in response:
    for obj in response["Contents"]:
        print(f"- Nombre: {obj['Key']}")
        print(f"  Tamaño: {obj['Size']} bytes")
        print(f"  Última modificación: {obj['LastModified']}")
else:
    print("No hay objetos en el bucket.")
