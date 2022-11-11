import os
import json
import threading
import time
import sys

#Recibe el la contraseña para la conexión a la base de datos MySQL por medio del primer parametro al ejecutar el scritp: python api.py contraseñamysql
PFXCLIENTCERTPWDVAR = sys.argv[1]
####!!!!!!!!!!!!!!PENDIENTE CAMBIAR TODOS LOS VALORES r00tr00t de este archivo por esta variable MYSQLPWDVAR

#Construir docker de nginx
#Instalar docker-compose
comando1 = 'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
comando2 = 'sudo chmod +x /usr/local/bin/docker-compose'
comando3 = 'docker-compose --version'

#'ocultar salida del comando os.system'
hideout = ' | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1'

os.system(comando1+hideout)
os.system(comando2+hideout)
os.system(comando3+hideout)

comando4a = 'sudo rm -rf ../docker/nginx/'
os.system(comando4a)

#Crear certificados
print("Creando Certificados externos que seran utilizados para conectarse al servidor nginx...")

comando4 = 'mkdir -p ../docker/nginx/certs'

#Crear certficado del servidor
comando8 = 'cd ../docker/nginx/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=nginx.d.local" -keyout /certs/server-key.pem -out /certs/server-cert.pem'

os.system(comando4)
os.system(comando8)

#Crear certificado del cliente
comando13 = 'cd ../docker/nginx/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=client1.d.local" -keyout /certs/client.key -out /certs/client.crt'

comando14 = 'cd ../docker/nginx/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=client1.d.local" -keyout /certs/client.key -out /certs/client.crt'

comando15 = 'cd ../docker/nginx/ && sudo chmod +r certs/client.key'

comando17 = 'cd ../docker/nginx/ && docker run --rm -v $PWD/certs:/certs -it nginx openssl pkcs12 -export -out /certs/client.pfx -inkey /certs/client.key -in /certs/client.crt -password pass:'+PFXCLIENTCERTPWDVAR+''

comando17b = 'cd ../docker/nginx/ && sudo chmod +r certs/client.*'
comando17c = 'mkdir -p Llaves && cp ../docker/nginx/certs/client.* Llaves/'

os.system(comando13)
os.system(comando14)
os.system(comando15)
os.system(comando17)
os.system(comando17b)
os.system(comando17c)
print("Certificados creados correctamente")
print("El certificado client.pfx es el que permite consumir las API a través del control de MUTUAL TLS, este debe ser cargado en al navegador a consumir la API o desde el script external_api.py que es el cliente final que consume el API")


#Crear archivo docker-compose para montar servidor nginx
comando18="""mkdir -p ../docker/nginx/sites-available && mkdir -p ../docker/nginx/conf.d && cat > ../docker/nginx/docker-compose.yml << EOF
version: "3"
services:
  web:
    image: nginx
    container_name: nginxReverseProxy
    ports:
      - 880:80
      - 4443:443
    volumes:
      - ./sites-available/:/etc/nginx/sites-available
      - ./certs/:/etc/ssl/selfsigned
      - ./conf.d/:/etc/nginx/conf.d
EOF"""
os.system(comando18)


obtenerIP = "hostname -I | awk '{print $1}'"
hostIP = os.popen(obtenerIP).read()[:-1]
#hostIP = str(os.system(obtenerIP))
print("La dirección IP es:"+hostIP)
#Crear archivo default con la configuración de servidor nginx
comando19="""cat > ../docker/nginx/conf.d/default.conf << EOF
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        # SSL configuration
        #
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
        ssl_certificate         /etc/ssl/selfsigned/server-cert.pem;
        ssl_certificate_key     /etc/ssl/selfsigned/server-key.pem;
        ssl_client_certificate  /etc/ssl/selfsigned/client.crt;
        ssl_verify_client       optional;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        #location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
        #       try_files $uri $uri/ =404;
        #}

        #https con mutual tls
        location /api {
                if (\$ssl_client_verify != "SUCCESS") { return 403; }
                proxy_pass https://"""+hostIP+""":10001/usuarios;
                #proxy_pass http://192.168.20.250:880/;
        }

        location /api_thirparties {
                if (\$ssl_client_verify != "SUCCESS") { return 403; }
                proxy_pass https://"""+hostIP+""":10002/usuarios;
                #proxy_pass http://testphp.vulnweb.com/;
        }

}
EOF"""
os.system(comando19)




#Crar contenedor de boveda hashicorp
comando20='cd ../docker/nginx/ && docker rm -f nginxReverseProxy'
comando21='cd ../docker/nginx/ && docker-compose up -d'
os.system(comando20)
os.system(comando21)