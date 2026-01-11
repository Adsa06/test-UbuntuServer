#!/bin/bash

set -e

echo "=============================="
echo "  SETUP UBUNTU SERVER + DOCKER"
echo "=============================="

# Comprobar que se ejecuta con sudo
if [ "$EUID" -ne 0 ]; then
  echo "Ejecuta este script con sudo"
  exit 1
fi

USER_NAME=${SUDO_USER}

echo "Usuario detectado: $USER_NAME"

echo "Actualizando sistema..."
apt update
apt upgrade -y
apt full-upgrade -y
apt autoremove -y

echo "Configurando zona horaria..."
timedatectl set-timezone Europe/Madrid

echo "Configurando idioma..."
locale-gen es_ES.UTF-8
update-locale LANG=es_ES.UTF-8

echo "Instalando utilidades basicas..."
apt install -y \
  curl \
  wget \
  git \
  ca-certificates \
  gnupg \
  lsb-release \
  apt-transport-https \
  software-properties-common \
  nano \
  htop \
  unzip \
  ufw

echo "Activando SSH..."
systemctl enable ssh
systemctl start ssh

echo "Configurando firewall UFW..."
ufw allow OpenSSH
ufw --force enable

echo "Eliminando posibles versiones antiguas de Docker..."
apt remove -y docker docker-engine docker.io containerd runc || true

echo "Agregando clave GPG de Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "Agregando repositorio oficial de Docker..."
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Instalando Docker y Docker Compose..."
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "Habilitando Docker al arranque..."
systemctl enable docker
systemctl start docker

echo "Agregando usuario al grupo docker..."
usermod -aG docker $USER_NAME

echo "Comprobando instalacion de Docker..."
docker --version
docker compose version

echo "=============================="
echo "INSTALACION COMPLETADA"
echo "Reinicia la maquina para aplicar cambios:"
echo "   sudo reboot"
echo "=============================="
