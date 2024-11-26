from models.tipo_producto import TipoProducto
from models.producto import Producto
from models.producto_ingrediente import ProductoIngrediente

from flask import Blueprint
producto_blueprint = Blueprint('producto_bp', __name__, url_prefix="/productos")

@producto_blueprint.route('/') 
def index():
    return "Controlador de Productos"