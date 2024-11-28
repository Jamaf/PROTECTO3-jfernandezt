from models.tipo_ingrediente import TipoIngrediente
from models.ingrediente import Ingrediente
from models.ingrediente import IngredienteSchema

from controllers.util import construir_rpta_json

from flask import Blueprint
ingrediente_blueprint = Blueprint('ingrediente_bp', __name__, url_prefix="/ingredientes")

@ingrediente_blueprint.route('/listado_ingredientes') 
def listado_ingredientes():
    '''Punto 5.8 Consultar todos los Ingredientes'''
    try:
        ingredientes = IngredienteSchema(many=True).dump(Ingrediente.traer_ingredientes())

        return construir_rpta_json( data = {"ingredientes" : ingredientes} )
    except Exception as exc:
        mensaje = f'Error obteniendo los ingredientes'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    
@ingrediente_blueprint.route('/consultar_por_id_o_nombre/<string:buscar_ingrediente>/') 
def consultar_por_id_o_nombre( buscar_ingrediente:str ):
    '''Punto 5.9 Consultar un ingrediente según su ID y Punto 5.10 Consultar un ingrediente según su nombre'''

    try:
        if buscar_ingrediente.isnumeric():
            ingrediente = IngredienteSchema().dump(Ingrediente.consultar_por_id(int(buscar_ingrediente)))
        else:
            ingrediente_bd =Ingrediente.consultar_por_nombre(buscar_ingrediente)
            if ingrediente_bd is None:
                raise ValueError
            ingrediente = IngredienteSchema().dump(ingrediente_bd)

        return construir_rpta_json( data = {"ingrediente" : ingrediente} )
    except Exception as exc:
        mensaje = f'El ingrediente no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
        
@ingrediente_blueprint.route('/consultar_es_sano_por_id/<int:id_ingrediente>/') 
def consultar_es_sano_por_id( id_ingrediente:int ):
    '''Punto 5.11 Consultar si un ingrediente es sano según su ID'''
    try:
        es_sano = Ingrediente.es_sano(id_ingrediente)
        return construir_rpta_json( data = {"es_sano" : es_sano} )
    except Exception as exc:
        mensaje = f'El id de ingrediente {id_ingrediente} no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )        

@ingrediente_blueprint.route('/reabastecer_por_id/<int:id_ingrediente>/')     
def reabastecer_por_id( id_ingrediente:int ):
    '''Punto 5.12 Reabastecer un ingrediente según su ID'''
    try:
        Ingrediente.abastecer_ingrediente(id_ingrediente)
        return construir_rpta_json( data = {"resultado" : "Ajuste realizado"} )
    except Exception as exc:
        mensaje = f'El id de ingrediente {id_ingrediente} no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )         
        
@ingrediente_blueprint.route('/renovar_inventario_por_id/<int:id_ingrediente>/')     
def renovar_inventario_por_id( id_ingrediente:int ):
    '''Punto 5.13 Renovar el inventario de un ingrediente según su ID '''
    try:
        Ingrediente.renovar_inventario(id_ingrediente)
        return construir_rpta_json( data = {"resultado" : "Ajuste realizado"} )
    except ValueError as err:
        mensaje = str(err)
        return construir_rpta_json( data = {"resultado" : mensaje} )    
    except Exception as exc:
        mensaje = f'El id de ingrediente {id_ingrediente} no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )         
                