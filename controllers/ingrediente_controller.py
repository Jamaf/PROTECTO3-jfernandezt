from models.tipo_ingrediente import TipoIngrediente
from models.ingrediente import Ingrediente

from flask import Blueprint
ingrediente_blueprint = Blueprint('ingrediente_bp', __name__, url_prefix="/ingredientes")

@ingrediente_blueprint.route('/') 
def index():
    return "Controlador de Ingredientes"