import boto3
from datetime import datetime, timedelta, timezone

REGION = "us-east-1"

ec2 = boto3.client("ec2", region_name=REGION)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)
s3 = boto3.client("s3")
autoscaling = boto3.client("autoscaling", region_name=REGION)


def listar_instancias_ec2():
    print("\n=== INSTANCIAS EC2 ===")
    response = ec2.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            state = instance["State"]["Name"]

            print(f"ID: {instance_id} | Tipo: {instance_type} | Estado: {state}")


def reporte_cpu_ec2():
    print("\n=== REPORTE CPU EC2 ÚLTIMAS 24 HORAS ===")

    response = ec2.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            metrics = cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[
                    {"Name": "InstanceId", "Value": instance_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=["Average"]
            )

            datapoints = metrics["Datapoints"]

            if datapoints:
                promedio = sum(point["Average"] for point in datapoints) / len(datapoints)
                print(f"Instancia: {instance_id} | CPU promedio 24h: {promedio:.2f}%")
            else:
                print(f"Instancia: {instance_id} | Sin métricas disponibles")


def listar_buckets_s3():
    print("\n=== BUCKETS S3 Y OBJETOS ===")

    response = s3.list_buckets()

    if not response["Buckets"]:
        print("No hay buckets S3 disponibles.")
        return

    for bucket in response["Buckets"]:
        bucket_name = bucket["Name"]
        print(f"\nBucket: {bucket_name}")

        try:
            objetos = s3.list_objects_v2(Bucket=bucket_name)

            if "Contents" in objetos:
                for obj in objetos["Contents"]:
                    print(f" - {obj['Key']} | Tamaño: {obj['Size']} bytes")
            else:
                print(" - Sin objetos")
        except Exception as e:
            print(f" - No se pudieron listar objetos: {e}")


def listar_auto_scaling():
    print("\n=== GRUPOS AUTO SCALING ===")

    response = autoscaling.describe_auto_scaling_groups()

    if not response["AutoScalingGroups"]:
        print("No hay grupos de Auto Scaling configurados.")
        return

    for group in response["AutoScalingGroups"]:
        print(f"""
Nombre: {group['AutoScalingGroupName']}
Mínimo: {group['MinSize']}
Máximo: {group['MaxSize']}
Deseado: {group['DesiredCapacity']}
""")


if __name__ == "__main__":
    listar_instancias_ec2()
    reporte_cpu_ec2()
    listar_buckets_s3()
    listar_auto_scaling()
