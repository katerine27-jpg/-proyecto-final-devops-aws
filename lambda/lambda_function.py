import json
import random

def lambda_handler(event, context):
    mensajes = [
        "Pipeline CI/CD ejecutado correctamente.",
        "Infraestructura DevOps desplegada en AWS.",
        "Monitoreo activo mediante CloudWatch.",
        "Automatización implementada con boto3.",
        "Microservicio DevOps funcionando correctamente."
    ]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "mensaje": random.choice(mensajes),
            "servicio": "microservicio-devops"
        })
    }
