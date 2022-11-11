from Jwencryption import *
import requests
import json
import os

os.system('reset')
registro = input("Ingrese el número del registro a consultar:")

#Recibir datos de un usuario especifico de la API api_thirdparties.py
requests.packages.urllib3.disable_warnings()


obtenerIP = "hostname -I | awk '{print $1}'"
hostIP = os.popen(obtenerIP).read()[:-1]
url = 'https://'+hostIP+':4443/api_thirparties/'+registro
print("")
print("Consultado la url: "+url)
print("")
#url = 'https://192.168.20.155:4443/api_thirparties/10'
#url = 'https://localhost:10002/usuarios/100'
#data = requests.get(url,verify=False) #
#Consumir el API con validación mutua a nivel de certificados (MUTUAL TLS)
data = requests.get(url,cert=('./Llaves/client.crt', './Llaves/client.key'),verify=False)
#convertimos la respuesta en json
usuarioConsultadoCifrado = data.json()

#Imprimir mensaje cifrado retornado al consultar un usuario con el API
print("")
print("Imprimiendo mensaje cifrado retornado al consultar un usuario con el API")
print(usuarioConsultadoCifrado)
print(type(usuarioConsultadoCifrado))


#Llamar la clase Jwencryption para descifrar la información que se recibira desde el api_thirdparties.py
#decryptjwt = Jwencryption("./keys/public.cert","./keys/private.key")
decryptjwt = Jwencryption("./Llaves/client.crt","./Llaves/client.key")


#Imprimir mensaje descifrado retornado al consultar un usuario con el API
print("")
print("Imprimiendo mensaje descifrado retornado al consultar un usuario con el API")
print("Para descifrar este mensaje se utiliza la llave privada client.key")
print("")
usuarioConsultadoDescifrado = decryptjwt.jwdecrypt(usuarioConsultadoCifrado)
#print(usuarioConsultadoDescifrado)
#Convertir dato de byte a string
payloadstring = usuarioConsultadoDescifrado.decode('utf-8')
print(payloadstring)
