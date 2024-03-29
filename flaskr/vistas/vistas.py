from re import U
from flask import request
from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema,ComentarioSchema, Comentario
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
comentario_schema = ComentarioSchema()


class VistaCanciones(Resource):

    def post(self):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self):
        return [cancion_schema.dump(ca) for ca in Cancion.query.all()]

class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo",cancion.titulo)
        cancion.minutos = request.json.get("minutos",cancion.minutos)
        cancion.segundos = request.json.get("segundos",cancion.segundos)
        cancion.interprete = request.json.get("interprete",cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '',204

class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]

class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}

class VistaUsuario(Resource):
    def get(self, id_usuario):
        return album_schema.dump(Usuario.query.get_or_404(id_usuario))

class VistaAlbumsUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]

class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)

        if "id_cancion" in request.json.keys():

            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else:
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]

class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo",album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204

class VistaCancionesCompartir(Resource):

    def put(self, cancionId):
        cancion = Cancion.query.get_or_404(cancionId)
        if "emails" in request.json.keys():
            email_list = request.json["emails"]
            user_list = email_list.split(',')
            print(user_list)
            users = Usuario.query.filter(Usuario.nombre.in_(user_list)).all()

            if len(users) <= 0:
                return "El usuario no existe", 404
            else:                
                for user in users:
                    print(user.nombre)
                    user.CancionesCompartidas.append(cancion)  
            db.session.commit()                              
        else:
            return "Al menos debe existir un email", 404

        return cancion_schema.dump(cancion)
        #return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}

class VistaAlbumesCompartir(Resource):

    def put(self, albumId):
        album = Album.query.get_or_404(albumId)
        if "emails" in request.json.keys():
            email_list = request.json["emails"]
            user_list = email_list.split(',')
            print(user_list)
            users = Usuario.query.filter(Usuario.nombre.in_(user_list)).all()

            if len(users) <= 0:
                return "El usuario no existe", 404
            else:
                for user in users:
                    print(user.nombre)
                    user.AlbumesCompartidos.append(album)
            db.session.commit()
        else:
            return "Al menos debe existir un email", 404

        return album_schema.dump(album)
        #return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
class VistaCancionFavorita(Resource):

    @jwt_required()
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [usuario_schema.dump(nv) for nv in cancion.favorita]
    
    def put(self, id_usuario, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        usuario = Usuario.query.get(id_usuario)
        if usuario is not None:            
            print(cancion.id)
            usuario.cancionFavorita.append(cancion)
            db.session.commit()
        else:
            return 'Usuario erróneo',404

        return cancion_schema.dump(cancion) 


class VistaComentarioAlbum(Resource):
    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        if "id_usuario" in request.json.keys():
            usuario = Usuario.query.get(request.json["id_usuario"])
            # print(usuario)
            if usuario is not None:
                usuario.cancionFavorita.append(cancion)
                db.session.commit()
            else:
                return 'Usuario erróneo',404
        return usuario_schema.dump(usuario)

class VistaEliminarFavorita(Resource):

    def delete(self, id_usuario, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.cancionFavorita.remove(cancion)
        db.session.commit()
        return usuario_schema.dump(usuario)

class VistaComentarioByIdComentario(Resource):
    def get(self, id_comentario):
        return comentario_schema.dump(Comentario.query.get_or_404(id_comentario))


class VistaComentarioAlbumByIdAlbum(Resource):
    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        nuevo_comentario = Comentario(comentario=request.json["comentario"], estado = request.json["estado"])
        nuevo_comentario.albumes.append(album)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return cancion_schema.dump(nuevo_comentario)

