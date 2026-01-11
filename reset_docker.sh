#!/bin/bash

echo "Deteniendo y eliminando contenedores, volúmenes y redes..."
docker compose down -v

echo "Limpiando contenedores, imágenes, redes y volúmenes sin usar..."
docker container prune -f
docker network prune -f
docker image prune -af
docker volume prune -f

echo "Reconstruyendo todas las imágenes y levantando servicios..."
docker compose up -d --build

# Espera para que la DB arranque (opcional)
echo "Esperando 10 segundos a que la base de datos arranque..."
sleep 10

echo "Proyecto levantado correctamente!"
echo "Verifica los contenedores activos con: docker compose ps"

echo "Lanzando Cloudflare Tunnel temporal..."
docker compose up -d cloudflared