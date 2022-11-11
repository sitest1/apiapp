import hvac
import os
import json
import threading
import time
import getpass

os.system('reset')
#Borar cualquier carpeta de contenedor que exista en la maquina
os.system('sudo rm -rf ../docker/*')
#Detener procesos de flask que puedan estar pegados
(os.system("fuser -k 10001/tcp"))
(os.system("fuser -k 10002/tcp"))
#Borar cualquier contenedor que exista en la maquina
os.system('docker rm -f $(docker ps -a -q) && sudo rm -rf ../docker')
os.system('reset')

print("POR FAVOR INTRODUZCA LAS CONTRASEÑAS REQUERIDAS PARA EL FUNCIONAMIENTO DEL PROGRAMA")
print("")
print("1: CREE LA CONTRASEÑA DE LA BASE DE DATOS: ")
print("")
print("En esta base de datos se almacenarán los datos descargados de la API: ")
print("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")
print("")
try:
    pMYSQL = getpass.getpass()
except Exception as error:
    print('ERROR', error)
else:
    #print('Password entered:', pMYSQL)
    print("")

print("2: CREE LA CONTRASEÑA DEL ARCHIVO client.pfx: ")
print("")
print("Este archivo corresponde a la llave privada y publica para que la aplicación")
print("external_api.py pueda consumir la API api_thirparties y pueda autenticarse ")
print("por certificados y posteriormente descifrar la información con su llave privada")
print("")
try:
    pPFX = getpass.getpass()
except Exception as error:
    print('ERROR', error)
else:
    #print('Password entered:', pPFX)
    print("")

#Variables requeridas para la ejecución del script
#Variable para asignar la clave que protegera la certificado pfx que permite consumir las APIs por MUTUAL TLS
PFXCLIENTCERTPWDVAR = pPFX

# 1) cargar la boveda hashicorp
print("")
print("Creando boveda hashicorp...")
print("")
comando1='python hvault_start.py'
#'ocultar salida del comando os.system'
hideout = ' | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1'
os.system(comando1+hideout)
print("")
print("Boveda hashicorp creada correctamente")
time.sleep(5)

#Cargar hvac para conectarse el vault http://localhost:8200 creado con Docker
client = hvac.Client(url='http://localhost:8200')
shares = 5
threshold = 3
result = client.sys.initialize(shares, threshold)
root_token = result['root_token']
#Keys de para hacer unseal
keys = result['keys']
#print(f"client.sys.is_initialized: {client.sys.is_initialized()}")


#Token de root
client.token = root_token

#Unseal vault
unseal_response1 = client.sys.submit_unseal_key(keys[0])
unseal_response2 = client.sys.submit_unseal_key(keys[1])
unseal_response3 = client.sys.submit_unseal_key(keys[2])
#print(f"client.sys.is_sealed: {client.sys.is_sealed()}")

#print(f"Is client authenticated: {client.is_authenticated()}")


#Crear engine secret donde se van almacenar las contraseñas
cmd = 'curl --header "X-Vault-Token: '+root_token+'" --request POST --data \'{ "type":"kv-v2" }\' http://127.0.0.1:8200/v1/sys/mounts/secret'
os.system(cmd+hideout)

#cmd2 = 'Token root: '+root_token
#print(root_token)
#print("cmd es igual a:"+cmd)
#os.system(cmd2)
###################################


#Funcion para crear llave en el vault
def write_secret():
    create_response = client.secrets.kv.v2.create_or_update_secret(path='mysql', secret=dict(mysqlpw=""+pMYSQL+""))
    #print(create_response)
write_secret()


#Funcion para leer la contraseña del vault
def read_secret():
    read_response = client.secrets.kv.read_secret_version(path='mysql')
    #print('{val}'.format(val=read_response['data']['data']['mysqlpw'],))
    global MYSQLPWVAR
    MYSQLPWVAR='{val}'.format(val=read_response['data']['data']['mysqlpw'],)
    #print(MYSQLPWVAR)
    #os.environ["MYSQLPWVAR"] = "HOLA MUNDO"
    #print(os.environ["MYSQLPWVAR"])

read_secret()


#Ejecutar el entorno:

# 2) cargar la base de datos MySQL cifrada en reposo que almacenara los datos consumidos de la API https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios
print("")
print("Creando base de datos MySQL con cifrado en reposo...")
print("")
comando2 = 'python mysql_start.py '+MYSQLPWVAR+'| sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1'
#os.system(comando2+hideout)
os.system(comando2+hideout)
print("Base de datos MySQL creada correctamente")

# 3) cargar servidor proxy reverso nginx que se encarga habilitar el consumo de los servicios api y api_thirdparties solicitando autenticación mutua a través de certificados (MUTUAL TLS). Este 
print("")
print("Iniciando Servidor NGINX de proxy reverso...")
print("")
comando5 = 'python nginx_start.py '+PFXCLIENTCERTPWDVAR+''
os.system(comando5+hideout)
print("Se cargaron los servicios descritos a continuacion, para consumirlos es necesario contar con el certificado client.pfx generado:")
print("")
obtenerIP = "hostname -I | awk '{print $1}'"
hostIP = os.popen(obtenerIP).read()[:-1]
print("Servicio 1: https://"+hostIP+":4443/api_thirparties")
print("Servicio 2: https://"+hostIP+":4443/api")

# 4) cargar la api.py que se encarga de permitir cargar datos a la bd mysql con el fin de persistirlos
print("")
print("Cargando servicio api.py...")
print("")
comando3 = 'nohup python api.py '+MYSQLPWVAR+' > log.txt 2>&1 &'
#comando3 = 'python api.py '+MYSQLPWVAR
threading.Thread(target=os.system(comando3)).start()
print("Servicio api.py creado correctamente")

# 5) cargar la api_thirdparties.py que se encarga de permitir consultar datos a la bd mysql desde terceros autorizados
print("")
print("Cargando servicio api_thirdparties.py...")
print("")
comando4 = 'nohup python api_thirdparties.py '+MYSQLPWVAR+' > log.txt 2>&1 &'
threading.Thread(target=os.system(comando4)).start()
print("Servicio api_thirdparties.py creado correctamente")
time.sleep(10)

# 6) cargar import.py que se encarga de tomar los datos de la API "https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios" y persistirlos en la BD MySQL a través de api.py
print("")
print("Cargando datos a la BD desde la API: https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios...")
print("")
comando6 = 'python import.py'
os.system(comando6+hideout)
print("Datos cargados correctamente en la BD desde la API: https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")
print("")
print("El archivo client.pfx quedo alojado en la carpeta LLaves del directorio actual de este programa")
print("Este archivo se encuentra protegido con la contraseña que definió al ejecutar este programa")