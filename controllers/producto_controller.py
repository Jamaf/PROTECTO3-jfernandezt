from models.producto import Producto
from models.producto import ProductoSchema

from flask import Blueprint
from flask import redirect
from flask import url_for
from flask_login import login_required
from flask_login import current_user

from controllers.util import construir_rpta_json
from urllib.parse import unquote

producto_blueprint = Blueprint('producto_bp', __name__, url_prefix="/productos")


@producto_blueprint.route('/listado_productos')
#@login_required la función listado de productos, no requiere que el usuario este autenticado
def listado_productos():
    '''Punto 5.1 Consultar todos los productos'''

    #pasos previos para hacer la autorización
    #print(current_user.rol.nombre)
    #print(current_user.rol.rol_modulo)
    #for var in  current_user.rol.rol_modulo:
    #    print(var.modulo.nombre)

    #lista = [rm.modulo.nombre for rm in current_user.rol.rol_modulo]
    #print(lista)
    #print(f"listado_productos => {current_user.tiene_habilitado_modulo('listado_productos')}")
    #print(f"listado_ingredientes =>  {current_user.tiene_habilitado_modulo('listado_ingredientes')}")
    #print(f"consultar_rentabilidad_por_id => {current_user.tiene_habilitado_modulo('consultar_rentabilidad_por_id')}")
    
    try:
        productos = ProductoSchema(many=True).dump(Producto.traer_todos())

        return construir_rpta_json( data = {"productos" : productos} )
    except Exception as exc:
        mensaje = f'Error obteniendo los productos'
        return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )


#Estas funciones comentadas son funcionales pero el profe comentó que intentaramos usar un solo endpoint
#para los puntos que buscan por id y por nombre
# @producto_blueprint.route('/consultar_por_id/<int:id_producto>/') 
# def consultar_por_id( id_producto:int ):
#     '''Punto 5.2 Consultar un producto según su ID'''
#     return ProductoSchema().jsonify(Producto.consultar_por_id(id_producto))

# @producto_blueprint.route('/consultar_por_nombre/<string:nombre_producto>/') 
# def consultar_por_nombre( nombre_producto:str ):
#     '''Punto 5.3 Consultar un producto según su nombre'''
    
#     return ProductoSchema().jsonify(Producto.consultar_por_nombre(nombre_producto))

@producto_blueprint.route('/consultar_por_id_o_nombre/<string:buscar_producto>/') 
@login_required
def consultar_por_id_o_nombre( buscar_producto:str ):
    '''Punto 5.2 Consultar un producto según su ID y Punto 5.3 Consultar un producto según su nombre'''
    
    if current_user.tiene_habilitado_modulo('Producto.consultar_por_id_o_nombre'):
        try:
            #separamos si vamos a buscar por nombre o por id
            if buscar_producto.isnumeric():
                producto = ProductoSchema().dump(Producto.consultar_por_id(int(buscar_producto)))
            else:
                #se greaga esta línea por que vercel esta metiendo como una doble codificación
                buscar_producto = buscar_producto.replace('%2520', '%20')
                producto_bd = Producto.consultar_por_nombre(unquote(buscar_producto))
                if producto_bd is None:
                    raise ValueError
                producto = ProductoSchema().dump(producto_bd)

            return construir_rpta_json( data = {"producto" : producto} )
        except Exception as exc:
            mensaje = f'El producto no fue encontrado'
            return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    else:
        return redirect(url_for('login_bp.no_autorizado'))   
     
@producto_blueprint.route('/consultar_calorias_por_id/<int:id_producto>/') 
@login_required
def consultar_calorias_por_id( id_producto:int ):
    '''Punto 5.4 Consultar las calorías de un producto según su ID'''
    if current_user.tiene_habilitado_modulo('Producto.consultar_calorias_por_id'):
        try:
            calorias = Producto.calcular_calorias(id_producto)
            return construir_rpta_json( data = {"calorias" : calorias} )
        except Exception as exc:
            mensaje = f'El id de producto {id_producto} no fue encontrado'
            return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    else:
        return redirect(url_for('login_bp.no_autorizado'))  
    
@producto_blueprint.route('/consultar_rentabilidad_por_id/<int:id_producto>/') 
@login_required
def consultar_rentabilidad_por_id( id_producto:int ):
    '''Punto 5.5 Consultar la rentabilidad de un producto según su ID'''
    if current_user.tiene_habilitado_modulo('Producto.consultar_rentabilidad_por_id'):
        try:
            rentabilidad = Producto.calcular_rentabilidad(id_producto)
            return construir_rpta_json( data = {"rentabilidad" : rentabilidad} )
        except Exception as exc:
            mensaje = f'El id de producto {id_producto} no fue encontrado'
            return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    else:
        return redirect(url_for('login_bp.no_autorizado'))  
    
@producto_blueprint.route('/consultar_costo_produccion_por_id/<int:id_producto>/') 
@login_required
def consultar_costo_produccion_por_id( id_producto:int ):
    '''Punto 5.6 Consultar el costo de producción de un producto según su ID'''
    if current_user.tiene_habilitado_modulo('Producto.consultar_costo_produccion_por_id'):
        try:
            costo_produccion = Producto.calcular_costo(id_producto)
            return construir_rpta_json( data = {"costo_produccion" : costo_produccion} )
        except Exception as exc:
            mensaje = f'El id de producto {id_producto} no fue encontrado'
            return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    else:
        return redirect(url_for('login_bp.no_autorizado'))  