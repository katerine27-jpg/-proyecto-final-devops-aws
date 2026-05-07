#!/bin/bash

echo "Actualizando paquetes del sistema..."
sudo yum update -y

echo "Verificando Python3..."
python3 --version

echo "Actualizando pip..."
python3 -m pip install --upgrade pip

echo "Instalando boto3..."
python3 -m pip install boto3

echo "Verificando instalación de boto3..."
python3 -c "import boto3; print('boto3 instalado correctamente')"

echo "Proceso setup completado."
