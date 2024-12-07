from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

#db = SQLAlchemy(app)
#Lo vamos a inciair sin app
#luego en el app.py se le configura
db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        #db.drop_all() #Si se quiere borrar las tablas de la BD
        db.create_all()

ma = Marshmallow()        

login_manager = LoginManager()

def load_models():
    from models.cliente import Cliente
    from models.usuario import Usuario
    from models.rol import Rol
    from models.modulo import Modulo
    from models.rol_modulo import RolModulo

    from models.tipo_ingrediente import TipoIngrediente
    from models.tipo_producto import TipoProducto
    from models.ingrediente import Ingrediente
    from models.producto import Producto
    from models.producto_ingrediente import ProductoIngrediente

    from models.heladeria_producto import HeladeriaProducto
    from models.heladeria import Heladeria
    from models.venta import Venta

    return [
        Cliente,
        Usuario,
        Rol,
        Modulo,
        RolModulo,
        TipoIngrediente,
        TipoProducto,
        Ingrediente,
        Producto,
        ProductoIngrediente,
        HeladeriaProducto,
        Heladeria,
        Venta
    ]