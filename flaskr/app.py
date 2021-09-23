from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import \
    VistaCanciones, \
    VistaCancion, \
    VistaSignIn, \
    VistaAlbum, \
    VistaAlbumsUsuario, \
    VistaCancionesAlbum, \
    VistaLogIn, \
    VistaAlbumesCanciones, \
    VistaCancionesCompartir, \
    VistaAlbumesCompartir, \
    VistaUsuario\
    ,VistaComentario, \
    VistaComentarioAlbum
    ,VistaComentario
    VistaEliminarFavorita, \
    VistaCancionFavorita, \
    VistaUsuario
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaCancionesCompartir, '/cancion/<int:cancionId>/compartir')
api.add_resource(VistaAlbumesCompartir, '/album/<int:albumId>/compartir')
api.add_resource(VistaComentarioAlbum,'/album/<int:id_album>/comentario')
api.add_resource(VistaComentario,'/comentario/<int:id_comentario>')
api.add_resource(VistaComentario,'/comentario')
api.add_resource(VistaCancionFavorita, '/cancion/<int:id_cancion>/favorita/')
api.add_resource(VistaEliminarFavorita, '/<int:id_usuario>/<int:id_cancion>/favorita/')
jwt = JWTManager(app)
