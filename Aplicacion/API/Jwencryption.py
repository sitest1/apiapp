#Realizar cifrado asimetrico JWE jwcrypto

#Relizar cifrado
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode, json_decode
import json 

#"Define una clase jwecnrypt para ser llamada desde otros archivos de python"
class Jwencryption:

    def __init__(self, publickeyIn, privatekeyIn):
        self.publickeyIn = publickeyIn
        self.privatekeyIn = privatekeyIn


    def jwencrypt(self, payloadIN):
        self.payloadIN = payloadIN
        #Abrir llaves publicas desde archivos de acuerdo a la ruta indicada en los parametros
        with open(self.publickeyIn, "rb") as pemfile:  #doctest: +SKIP
            public_key = jwk.JWK.from_pem(pemfile.read())

        with open(self.privatekeyIn, "rb") as pemfile:  #doctest: +SKIP
            private_key = jwk.JWK.from_pem(pemfile.read())

        #payload = {"fec_alta":"2021-07-31T00:11:06.741Z","user_name":"Junior39","codigo_zip":"22139","credit_card_num":"6767-2293-4172-5169","credit_card_ccv":"357","cuenta_numero":"50099904","direccion":"Amelia Forks","geo_latitud":"-40.0728","geo_longitud":"-39.5073","color_favorito":"white","foto_dni":"http://placeimg.com/640/480","ip":"224.140.175.223","auto":"Bugatti Corvette","auto_modelo":"Challenger","auto_tipo":"Cargo Van","auto_color":"Lamborghini PT Cruiser","cantidad_compras_realizadas":30564,"avatar":"https://cdn.fakercloud.com/avatars/franciscoamk_128.jpg","fec_birthday":"2022-03-29T03:28:16.364Z","id":"2"}
        payload = self.payloadIN
        protected_header = {"alg": "RSA-OAEP-256","enc": "A256CBC-HS512","typ": "JWE","kid": public_key.thumbprint()}
        jwetoken = jwe.JWE(json_encode(payload),recipient=public_key,protected=protected_header)
        #jwetoken = jwe.JWE(payload.encode('utf-8'),recipient=public_key,protected=protected_header)
        enc = jwetoken.serialize()
        


        #Realizar descifrado
        jwetoken = jwe.JWE()
        jwetoken.deserialize(enc, key=private_key)
        payload = jwetoken.payload

        """
        #########Imprimir resultados para modo debug

        print("Mensaje Cifrado Asimetrico:")
        print(enc)
        print(type(enc))
        print("")        
        

        print("Descifrando mensaje Asimetrico")
        print(payload)
        print(type(payload))
        #Convertir payload de byte a string
        payloadstring = payload.decode('utf-8')
        print(payloadstring)
        print(type(payloadstring))
        #Convertir payload de string a json
        payloadjson = json.loads(payloadstring)
        print(payloadjson)
        print(type(payloadjson))
        #############################################
        """

        #Returnar mensaje cifrado como tipo string
        return enc


    def jwdecrypt(self, encIn):

            enc = encIn
            #Abrir llaves publicas desde archivos de acuerdo a la ruta indicada en los parametros
            with open(self.publickeyIn, "rb") as pemfile:  #doctest: +SKIP
                public_key = jwk.JWK.from_pem(pemfile.read())

            with open(self.privatekeyIn, "rb") as pemfile:  #doctest: +SKIP
                private_key = jwk.JWK.from_pem(pemfile.read())

            #payload = {"fec_alta":"2021-07-31T00:11:06.741Z","user_name":"Junior39","codigo_zip":"22139","credit_card_num":"6767-2293-4172-5169","credit_card_ccv":"357","cuenta_numero":"50099904","direccion":"Amelia Forks","geo_latitud":"-40.0728","geo_longitud":"-39.5073","color_favorito":"white","foto_dni":"http://placeimg.com/640/480","ip":"224.140.175.223","auto":"Bugatti Corvette","auto_modelo":"Challenger","auto_tipo":"Cargo Van","auto_color":"Lamborghini PT Cruiser","cantidad_compras_realizadas":30564,"avatar":"https://cdn.fakercloud.com/avatars/franciscoamk_128.jpg","fec_birthday":"2022-03-29T03:28:16.364Z","id":"2"}
            #payload = self.payloadIN
            protected_header = {"alg": "RSA-OAEP-256","enc": "A256CBC-HS512","typ": "JWE","kid": public_key.thumbprint()}
                


            #Realizar descifrado
            jwetoken = jwe.JWE()
            jwetoken.deserialize(enc, key=private_key)
            payload = jwetoken.payload
            #Returnar mensaje cifrado como tipo string
            return payload


#public_key = jwk.JWK()
#private_key = jwk.JWK.generate(kty='RSA', size=2048)
#public_key.import_key(**json_decode(private_key.export_public()))




