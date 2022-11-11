from flask import Flask
from flask import request
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_restful import Api, Resource
from Jwencryption import *
import sys

#Imprimir argmentos recibidos al ejecutar este script de python: python api.py parametro1
#Imprimir argumento 1
#print(sys.argv[1])
#Imprimir argumento 2
#print(sys.argv[2])

#Recibe el la contraseña para la conexión a la base de datos MySQL por medio del primer parametro al ejecutar el scritp: python api.py contraseñamysql
MYSQLPWDVAR = sys.argv[1]

app = Flask(__name__)
with app.app_context():
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password123!@localhost/mydatabase2'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:r00tr00t@server1.example.com/mydatabase2?ssl_ca=keys/root-ca.pem'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:r00tr00t@mysql.d.local/mydatabase3?ssl_ca=keys/root-ca.pem'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+MYSQLPWDVAR+'@mysql.d.local/mydatabase3?ssl_ca=./keys/root-ca.pem'
    db = SQLAlchemy(app) 
    ma = Marshmallow(app)
    #Configuración de la base de datos


    api = Api(app)

    #Crear modelo (tabla) en la base de datos
    #class Usuario(db.Model):
    #    id = db.Column(db.Integer, primary_key = True)
    #    titulo = db.Column( db.String(50) )
    #    contenido = db.Column( db.String(255) )


    class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        fec_alta = db.Column( db.String(50) )
        user_name = db.Column( db.String(255) )
        codigo_zip = db.Column( db.String(255) )
        credit_card_num = db.Column( db.String(255) )
        credit_card_ccv = db.Column( db.String(255) )
        cuenta_numero = db.Column( db.String(255) )
        direccion = db.Column( db.String(255) )
        geo_latitud = db.Column( db.String(255) )
        geo_longitud = db.Column( db.String(255) )
        color_favorito = db.Column( db.String(255) )
        foto_dni = db.Column( db.String(255) )
        ip = db.Column( db.String(255) )
        auto = db.Column( db.String(255) )
        auto_modelo = db.Column( db.String(255) )
        auto_tipo = db.Column( db.String(255) )
        auto_color = db.Column( db.String(255) )
        cantidad_compras_realizadas = db.Column( db.String(255) )
        avatar = db.Column( db.String(255) )
        fec_birthday = db.Column( db.String(255) )

#db.create_all()



class Usuario_Schema(ma.Schema):
    class Meta:
        fields = ("id", "fec_alta", "user_name", "codigo_zip", "credit_card_num", "credit_card_ccv", "cuenta_numero", "direccion", "geo_latitud", "geo_longitud", "color_favorito", "foto_dni", "ip", "auto", "auto_modelo", "auto_tipo", "auto_color", "cantidad_compras_realizadas", "avatar", "fec_birthday")

post_schema = Usuario_Schema()
posts_schema = Usuario_Schema(many = True)


#Clase para generar GET PUT UPDATE DELETE hacia la base de datos
class RecursoListarUsuarios(Resource):

#Listar todas las publicaciones de la base de datos

    def get(self):
        Usuarios = Usuario.query.all()
        return posts_schema.dump(Usuarios)


"""
#Agregar nuevos registros a la base de datos
    def post(self):
            nuevo_usuario = Usuario(
                fec_alta = request.json['fec_alta'],
                user_name = request.json['user_name'],
                codigo_zip = request.json['codigo_zip'],
                credit_card_num = request.json['credit_card_num'],
                credit_card_ccv = request.json['credit_card_ccv'],
                cuenta_numero = request.json['cuenta_numero'],
                direccion = request.json['direccion'],
                geo_latitud = request.json['geo_latitud'],
                geo_longitud = request.json['geo_longitud'],
                color_favorito = request.json['color_favorito'],
                foto_dni = request.json['foto_dni'],
                ip = request.json['ip'],
                auto = request.json['auto'],
                auto_modelo = request.json['auto_modelo'],
                auto_tipo = request.json['auto_tipo'],
                auto_color = request.json['auto_color'],
                cantidad_compras_realizadas = request.json['cantidad_compras_realizadas'],
                avatar = request.json['avatar'],
                fec_birthday = request.json['fec_birthday']
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return post_schema.dump(nuevo_usuario)
"""

#Listar publicación especifica
class RecursoUnUsuario(Resource):
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuarioConsultado = post_schema.dump(usuario)
        print("")
        print("Imprimiendo mensaje sin cifrado retornado al consultar un usuario con el API")
        print(usuarioConsultado)
        print(type(usuarioConsultado))
        
        #Llamar la clase Jwencryption para cifrar la información que se enviara al cliente que consume el API
        #encryptjwt = Jwencryption("./keys/public.cert","./keys/private.key")
        encryptjwt = Jwencryption("./Llaves/client.crt","./Llaves/client.key")
        
        #Imprimir mensaje cifrado retornado al consultar un usuario con el API
        print("")
        print("Imprimiendo mensaje cifrado retornado al consultar un usuario con el API")
        usuarioConsultadoCifrado = encryptjwt.jwencrypt(usuarioConsultado)
        print(usuarioConsultadoCifrado)
        print(type(usuarioConsultadoCifrado))
        print("Imprimiendo mensaje cifrado en modo json retornado al consultar un usuario con el API")
        print()
        print(type(json.loads(usuarioConsultadoCifrado)))

        """
        #Imprimir mensaje descifrado retornado al consultar un usuario con el API
        print("")
        print("Imprimiendo mensaje descifrado retornado al consultar un usuario con el API")
        usuarioConsultadoDescifrado = encryptjwt.jwdecrypt(usuarioConsultadoCifrado)
        #print(usuarioConsultadoDescifrado)
        #Convertir dato de byte a string
        payloadstring = usuarioConsultadoDescifrado.decode('utf-8')
        print(payloadstring)
        """

        #return post_schema.dump(usuario)
        return usuarioConsultadoCifrado

       

        
        

        

"""
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)

        if 'fec_alta' in request.json:
            usuario.fec_alta = request.json['fec_alta']
        if 'user_name' in request.json:
            usuario.user_name = request.json['user_name']
        if 'codigo_zip' in request.json:
            usuario.codigo_zip = request.json['codigo_zip']
        if 'credit_card_num' in request.json:
            usuario.credit_card_num = request.json['credit_card_num']
        if 'credit_card_ccv' in request.json:
            usuario.credit_card_ccv = request.json['credit_card_ccv']
        if 'cuenta_numero' in request.json:
            usuario.cuenta_numero = request.json['cuenta_numero']
        if 'direccion' in request.json:
            usuario.direccion = request.json['direccion']
        if 'geo_latitud' in request.json:
            usuario.geo_latitud = request.json['geo_latitud']
        if 'geo_longitud' in request.json:
            usuario.geo_longitud = request.json['geo_longitud']
        if 'color_favorito' in request.json:
            usuario.color_favorito = request.json['color_favorito']
        if 'foto_dni' in request.json:
            usuario.foto_dni = request.json['foto_dni']
        if 'ip' in request.json:
            usuario.ip = request.json['ip']
        if 'auto' in request.json:
            usuario.auto = request.json['auto']
        if 'auto_modelo' in request.json:
            usuario.auto_modelo = request.json['auto_modelo']
        if 'auto_tipo' in request.json:
            usuario.auto_tipo = request.json['auto_tipo']
        if 'auto_color' in request.json:
            usuario.auto_color = request.json['auto_color']
        if 'cantidad_compras_realizadas' in request.json:
            usuario.cantidad_compras_realizadas = request.json['cantidad_compras_realizadas']
        if 'avatar' in request.json:
            usuario.avatar = request.json['avatar']
        if 'fec_birthday' in request.json:
            usuario.fec_birthday = request.json['fec_birthday']

        db.session.commit()
        return post_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
"""

# Líneas nuevas, se agrega una nueva ruta         
api.add_resource(RecursoListarUsuarios, '/usuarios')
api.add_resource(RecursoUnUsuario,'/usuarios/<int:id_usuario>')


if __name__ == '__main__':
    #app.run(host="localhost", port=10002, debug=True)
    app.run(host='0.0.0.0', port=10002, debug=True, ssl_context='adhoc')
