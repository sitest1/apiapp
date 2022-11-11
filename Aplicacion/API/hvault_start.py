import os
import json
import threading
import time
import sys

#Recibe el la contraseña para la conexión a la base de datos MySQL por medio del primer parametro al ejecutar el scritp: python api.py contraseñamysql
#MYSQLPWDVAR = sys.argv[1]
####!!!!!!!!!!!!!!PENDIENTE CAMBIAR TODOS LOS VALORES r00tr00t de este archivo por esta variable MYSQLPWDVAR

#Construir docker de hashicorp vault
#Instalar docker-compose
comando1 = 'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose  > /dev/null'
comando2 = 'sudo chmod +x /usr/local/bin/docker-compose'
comando3 = 'docker-compose --version'

#'ocultar salida del comando os.system'
hideout = ' | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1'

os.system(comando1+hideout)
os.system(comando2+hideout)
os.system(comando3+hideout)


#Crear archivo docker-compose para montar la boveda hashicorp
comando4="""sudo rm -rf ../docker/vault && mkdir -p ../docker/vault/volumes/config && mkdir -p ../docker/vault/volumes/file && mkdir -p ../docker/vault/volumes/logs} && cat > ../docker/vault/docker-compose.yml << EOF
version: '2'
services:
  vault:
    image: vault
    container_name: vault
    ports:
      - "8200:8200"
    restart: always
    volumes:
      - ./volumes/logs:/vault/logs
      - ./volumes/file:/vault/file
      - ./volumes/config:/vault/config
    cap_add:
      - IPC_LOCK
    entrypoint: vault server -config=/vault/config/vault.json
EOF"""
os.system(comando4)

#Crear archivo vault.json con la configuración de la boveda hashicorp
comando5="""cat > ../docker/vault/volumes/config/vault.json << EOF
{
  "backend": {
    "file": {
      "path": "/vault/file"
    }
  },
  "listener": {
    "tcp":{
      "address": "0.0.0.0:8200",
      "tls_disable": 1
    }
  },
  "ui": true
}
EOF"""
os.system(comando5)



#Crar contenedor de boveda hashicorp
comando6='cd ../docker/vault/ && docker rm -f vault'
comando7='cd ../docker/vault/ && docker-compose up -d'
os.system(comando6)
os.system(comando7)