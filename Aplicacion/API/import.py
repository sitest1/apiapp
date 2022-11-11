#Importar la librería requests
import requests
import json
import os

#Aviso para mostrar que se esta consumiendo un API
print("Obteniendo información del API....")

#URL de la API
API = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
data = requests.get(API)

#convertimos la respuesta en json
data = data.json()

#bucle de iteración sobre datos
#for element in data:
#    print(element['user_name'])
#    print(element['credit_card_num'])
requests.packages.urllib3.disable_warnings()

"""#Validación de que esta retornando la información correctamente
##############################################################################

print("")
print("Imprimiento primero registro obtenido")
print(data[0])
print("")
print("Imprimiento atributo user_name del primer registro obtenido")
print(data[0]['user_name'])
print(type(data[0]))

print("")
print("Imprimiento segundo registro obtenido")
print(data[1])
print("")
print("Imprimiento atributo user_name del segundo registro obtenido")
print(data[1]['user_name'])
print(type(data[1]))
#print(data[0]['credit_card_num'])

print("")
print("Imprimiento registro convertido a string")
datastring = json.dumps(data[2])
print(datastring)
print(type(datastring))

##############################################################################
"""

"""#Enviar datos de un usuario a la base de datos a través de la API api.py
#curl -d data[1] -H "Content-Type:application/json" -X POST http://localhost:10001/usuarios
url = 'http://localhost:10001/usuarios'
headers = {'Content-type': 'application/json'}
payload = json.dumps(data[3])
requests.post(url, headers=headers, data=payload)
"""

#Enviar datos de todos los usuarios a la base de datos a través de la API api.py
#curl -d data[1] -H "Content-Type:application/json" -X POST http://localhost:10001/usuarios
#url = 'https://localhost:10001/usuarios'

obtenerIP = "hostname -I | awk '{print $1}'"
hostIP = os.popen(obtenerIP).read()[:-1]

url = 'https://'+hostIP+':4443/api'
headers = {'Content-type': 'application/json'}
payload = json.dumps(data[3])
#requests.post(url, headers=headers, data=payload,verify=False) 
#Consumir el API con validación mutua a nivel de certificados (MUTUAL TLS)
requests.post(url, cert=('./Llaves/client.crt', './Llaves/client.key'), headers=headers, data=payload,verify=False) 

#bucle de iteración sobre datos
for element in data:
    #print(element['user_name'])
    #print(element['credit_card_num'])
    payload = json.dumps(element)
    #requests.post(url, headers=headers, data=payload,verify=False) 
    #Consumir el API con validación mutua a nivel de certificados (MUTUAL TLS)
    requests.post(url, cert=('./Llaves/client.crt', './Llaves/client.key'), headers=headers, data=payload,verify=False)
