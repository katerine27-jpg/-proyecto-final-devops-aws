#!/bin/bash

LOG_DIR="$HOME/environment/logs"

mkdir -p "$LOG_DIR"

echo "Ejecutando limpieza de logs: $(date)" >> "$LOG_DIR/limpieza.log"

find "$LOG_DIR" -type f -name "*.log" -mtime +7 -delete

echo "Limpieza finalizada: $(date)" >> "$LOG_DIR/limpieza.log"
