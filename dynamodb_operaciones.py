import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
TABLE_NAME = "devops-tabla"

dynamodb = boto3.resource("dynamodb", region_name=REGION)

try:
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    print(f"Creando tabla: {TABLE_NAME}")
    table.wait_until_exists()
    print("Tabla creada correctamente.")

except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceInUseException":
        print(f"La tabla {TABLE_NAME} ya existe. Se continuará usando la tabla existente.")
        table = dynamodb.Table(TABLE_NAME)
    else:
        raise

table = dynamodb.Table(TABLE_NAME)

item = {
    "id": "001",
    "nombre": "Registro de prueba DevOps",
    "status": "creado"
}

table.put_item(Item=item)
print("Registro insertado correctamente.")

table.update_item(
    Key={"id": "001"},
    UpdateExpression="SET #st = :nuevo_status",
    ExpressionAttributeNames={
        "#st": "status"
    },
    ExpressionAttributeValues={
        ":nuevo_status": "actualizado"
    }
)
print("Registro actualizado correctamente.")

table.delete_item(
    Key={"id": "001"}
)
print("Registro eliminado correctamente.")
