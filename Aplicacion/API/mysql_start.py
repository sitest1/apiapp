import os
import json
import threading
import time
import sys

#Recibe el la contraseña para la conexión a la base de datos MySQL por medio del primer parametro al ejecutar el scritp: python api.py contraseñamysql
MYSQLPWDVAR = sys.argv[1]
#MYSQLPWDVAR = "rootroot"
####!!!!!!!!!!!!!!PENDIENTE CAMBIAR TODOS LOS VALORES r00tr00t de este archivo por esta variable MYSQLPWDVAR

#Construir docker de mysql

#Instalar docker-compose
comando1 = 'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
comando2 = 'sudo chmod +x /usr/local/bin/docker-compose'
comando3 = 'docker-compose --version'

#'ocultar salida del comando os.system'
hideout = ' | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1'

os.system(comando1+hideout)
os.system(comando2+hideout)
os.system(comando3+hideout)

#Crear certificados
print("Creando Certificados internos que seran utilizados para conectarse a la BD MySQL a través de TLS...")
comando4 = 'mkdir -p ../docker/mysql2/certs'
#Crear certificado de la CA
comando5 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl genrsa 2048 > certs/root-ca-key.pem'
comando6 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl req -new -x509 -nodes -days 3600 -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=d.local" -key /certs/root-ca-key.pem -out /certs/root-ca.pem'
#Copiar certificado de la CA en la carpeta keys que es donde llaman las llaves las APIs
#Este certificado es utilizado por las apis para conectarse a la base de datos por TLS 
comando7 = 'mkdir keys && cp ../docker/mysql2/certs/root-ca.pem keys/'
#Crear certficado del servidor
comando8 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl req -newkey rsa:2048 -days 3600 -nodes -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=mysql.d.local" -keyout /certs/server-key.pem -out /certs/server-req.pem'
comando9 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl rsa -in /certs/server-key.pem -out /certs/server-key.pem'
comando10 = 'cd ../docker/mysql2/ && sudo chmod +r certs/server-key.pem'
comando11 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl x509 -req -in /certs/server-req.pem -days 3600 -CA /certs/root-ca.pem -CAkey /certs/root-ca-key.pem -set_serial 01 -out /certs/server-cert.pem'
comando12 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl verify -CAfile /certs/root-ca.pem /certs/server-cert.pem'
os.system(comando4)
os.system(comando5)
os.system(comando6)
os.system(comando7)
os.system(comando8)
os.system(comando9)
os.system(comando10)
os.system(comando11)
os.system(comando12)

#Crear certificado del cliente
comando13 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl req -newkey rsa:2048 -days 3600 -nodes -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=client1.d.localg" -keyout /certs/client-key.pem -out /certs/client-req.pem'
comando14 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl rsa -in /certs/client-key.pem -out /certs/client-key.pem'
comando15 = 'cd ../docker/mysql2/ && sudo chmod +r certs/client-key.pem'
comando16 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl x509 -req -in /certs/client-req.pem -days 3600 -CA /certs/root-ca.pem -CAkey /certs/root-ca-key.pem -set_serial 01 -out /certs/client-cert.pem'
comando17 = 'cd ../docker/mysql2/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl verify -CAfile /certs/root-ca.pem /certs/client-cert.pem'
os.system(comando13)
os.system(comando14)
os.system(comando15)
os.system(comando16)
os.system(comando17)
print("Certificados creados correctamente")

#Crear archivo docker-compose para montar la base de datos mysql
comando18="""sudo rm -rf ../docker/mysql2/database && mkdir -p ../docker/mysql2/database && cat > ../docker/mysql2/docker-compose.yml << EOF
version: '3.8'

services:

    mysql:
        image: "mysql/mysql-server:8.0.21"
        container_name: mysql2
        command: [ "mysqld",
                    "--character-set-server=utf8mb4",
                    "--collation-server=utf8mb4_unicode_ci",
                    "--bind-address=0.0.0.0",
                    "--require_secure_transport=ON",
                    "--ssl-ca=/etc/certs/root-ca.pem",
                    "--ssl-cert=/etc/certs/server-cert.pem",
                    "--ssl-key=/etc/certs/server-key.pem",
                    "--plugin-load-add=keyring_file.so",
                    "--default_authentication_plugin=mysql_native_password" ]
        ports:
            - "3306:3306"
        volumes:
            - type: bind
              source: ./database
              target: /var/lib/mysql
            - type: bind
              source: ./certs
              target: /etc/certs/
        restart: always
        environment:
           MYSQL_ROOT_PASSWORD: """+MYSQLPWDVAR+"""
           MYSQL_ROOT_HOST: "%"
EOF"""
os.system(comando18)
#Crar contenedor de base de daatos
comando19='cd ../docker/mysql2/ && docker rm -f mysql2'
comando20='cd ../docker/mysql2/ && docker-compose up -d'
os.system(comando19)
os.system(comando20)
#COMANDO PARA CREAR BASE DE DATOS mydatabase3 CIFRADA
comando21="cd ../docker/mysql2/ && mysql --host 127.0.0.1 -P 3306 -u root -p"+MYSQLPWDVAR+" --ssl-ca=./certs/root-ca.pem --execute=\"CREATE SCHEMA mydatabase3 DEFAULT ENCRYPTION='y';\""
#Esperando a que la base de datos carge por completo
print("Esperando a que la base de datos carge por completo...")
time.sleep(60)
print("Cifrando la base de datos en reposo...")
os.system(comando21)