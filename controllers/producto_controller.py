from models.tipo_producto import TipoProducto
from models.producto import Producto, ProductoSchema
from models.producto_ingrediente import ProductoIngrediente

from controllers.util import construir_rpta_json

from flask import Blueprint
producto_blueprint = Blueprint('producto_bp', __name__, url_prefix="/productos")


@producto_blueprint.route('/listado_productos') 
def listado_productos():
    '''Punto 5.1 Consultar todos los productos'''
    try:
        productos = ProductoSchema(many=True).dump(Producto.traer_todos())

        return construir_rpta_json( data = {"productos" : productos} )
    except Exception as exc:
        mensaje = f'Error obteniendo los productos'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    
# @producto_blueprint.route('/consultar_por_id/<int:id_producto>/') 
# def consultar_por_id( id_producto:int ):
#     '''Punto 5.2 Consultar un producto según su ID'''
#     return ProductoSchema().jsonify(Producto.consultar_por_id(id_producto))

# @producto_blueprint.route('/consultar_por_nombre/<string:nombre_producto>/') 
# def consultar_por_nombre( nombre_producto:str ):
#     '''Punto 5.3 Consultar un producto según su nombre'''
    
#     return ProductoSchema().jsonify(Producto.consultar_por_nombre(nombre_producto))

@producto_blueprint.route('/consultar_por_id_o_nombre/<string:buscar_producto>/') 
def consultar_por_id_o_nombre( buscar_producto:str ):
    '''Punto 5.2 Consultar un producto según su ID y Punto 5.3 Consultar un producto según su nombre'''

    try:
        if buscar_producto.isnumeric():
            producto = ProductoSchema().dump(Producto.consultar_por_id(int(buscar_producto)))
        else:
            producto_bd =Producto.consultar_por_nombre(buscar_producto)
            if producto_bd is None:
                raise ValueError
            producto = ProductoSchema().dump(producto_bd)

        return construir_rpta_json( data = {"producto" : producto} )
    except Exception as exc:
        mensaje = f'El producto no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    
@producto_blueprint.route('/consultar_calorias_por_id/<int:id_producto>/') 
def consultar_calorias_por_id( id_producto:int ):
    '''Punto 5.4 Consultar las calorías de un producto según su ID'''
    try:
        calorias = Producto.calcular_calorias(id_producto)
        return construir_rpta_json( data = {"calorias" : calorias} )
    except Exception as exc:
        mensaje = f'El id de producto {id_producto} no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )

@producto_blueprint.route('/consultar_rentabilidad_por_id/<int:id_producto>/') 
def consultar_rentabilidad_por_id( id_producto:int ):
    '''Punto 5.5 Consultar la rentabilidad de un producto según su ID'''
    try:
        rentabilidad = Producto.calcular_rentabilidad(id_producto)
        return construir_rpta_json( data = {"rentabilidad" : rentabilidad} )
    except Exception as exc:
        mensaje = f'El id de producto {id_producto} no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )

@producto_blueprint.route('/consultar_costo_produccion_por_id/<int:id_producto>/') 
def consultar_costo_produccion_por_id( id_producto:int ):
    '''Punto 5.6 Consultar el costo de producción de un producto según su ID'''
    try:
        costo_produccion = Producto.calcular_costo(id_producto)
        return construir_rpta_json( data = {"costo_produccion" : costo_produccion} )
    except Exception as exc:
        mensaje = f'El id de producto {id_producto} no fue encontrado'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
