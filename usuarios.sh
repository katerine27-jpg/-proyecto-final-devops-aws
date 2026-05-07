#!/bin/bash

echo "Creando grupo devops..."
sudo groupadd devops 2>/dev/null || echo "El grupo ya existe"

echo "Creando usuario devops_user..."
sudo useradd devops_user 2>/dev/null || echo "El usuario ya existe"

echo "Agregando usuario al grupo devops..."
sudo usermod -aG devops devops_user

echo "Asignando permisos sobre ~/environment..."
sudo chown -R devops_user:devops ~/environment
sudo chmod -R 775 ~/environment

echo "Restaurando permisos para ec2-user..."
sudo chown -R ec2-user:ec2-user ~/environment

echo "Gestión de usuarios y permisos completada."


