from models.heladeria import Heladeria
from models.producto import Producto
from models.ingrediente import Ingrediente

from flask import Blueprint
from flask import redirect
from flask import url_for
from flask_login import login_required
from flask_login import current_user
from flask import render_template

from controllers.util import construir_rpta_json

heladeria_blueprint = Blueprint('heladeria_bp', __name__, url_prefix="/")

#El método vender_por_id se creo para la API solicitada en el Proyecto 3
#Al ser de una API su rpta es un JSON en el formato estandarizado para toda la API
@heladeria_blueprint.route('/vender_por_id/<int:id>/')
@login_required
def vender_por_id(id:int):
    '''Punto 5.7 Vender un producto según su ID'''
    if current_user.tiene_habilitado_modulo('Heladeria.vender_por_id'):    
        try:
            mensaje = Heladeria.vender_producto(id)
            return construir_rpta_json( data = {"resultado_venta" : mensaje} )        
        except ValueError as err:
            mensaje = str(err)
            return construir_rpta_json( data = {"resultado_venta" : mensaje} )
        except Exception as err:
            mensaje = mensaje = f'El id de producto {id} no fue encontrado'
            return construir_rpta_json( data = None, error_message = mensaje, cod_error = 404 )
    else:
        return redirect(url_for('login_bp.no_autorizado'))

# TODOS los métodos a continuacion se diseñaron para la Interfaz WEB
# Que se trabajó en el proyecto 2
# Para esta entrega, se le agrega autenticación y autorización 

@heladeria_blueprint.route('/') 
def index():
    ''' Este método se diseño junto a la interfaz web para la entrega del proyecto 2.
        Equivale a 5.1 Consultar todos los productos, por ende, no se le habilita autenticación.
        Es importante anotar que para la heladería web se muestran 
        solo los productos habilitados para la heladeria, 
        mientras que la API muestra todos los productos del sistema
    '''

    productos_activos = Heladeria.traer_productos_habilitados()
    return render_template('index.html', productos=productos_activos)

@heladeria_blueprint.route('/gestion')
def gestion_home():
    '''Se muestran algunas funcionalidades de la heladería web como:
            * Informe de Ventas Realizadas
            * Ver Inventario de Ingredientes
            * Abastecer Ingredientes
            * Renovar Inventario de Ingredientes
            * Validar Producto Más Rentable       
        Este listado se podría armar dinámicamente trayendo los módulos habilitados para el rol
        Pero se deja fijo para que sea fácil la visualización de la página "login_bp.no_autorizado"
    '''
    return render_template('gestion.html')    

@heladeria_blueprint.route('/vender/<int:id>/')
@login_required
def vender(id:int):
    '''Metodo que realiza la venta de un producto para la interfaz web
       Este método se diseño junto a la interfaz web para la entrega del proyecto 2
    '''
    if current_user.tiene_habilitado_modulo('Heladeria.vender'):    
        resultado:str

        try:
            resultado = Heladeria.vender_producto(id)
            #print(f'Calorias { Producto.calcular_calorias(id)}')
            print(f'Costo Producción { Producto.calcular_costo(id)}')
            
        except ValueError as err:
            resultado = str(err)

        producto = Producto.consultar_por_id(id)

        return render_template('venta_detalle.html', resultado = resultado, producto=producto)    
    else:
        return redirect(url_for('login_bp.no_autorizado'))
    
@heladeria_blueprint.route('/informe_ventas')
@login_required
def informe_ventas():
    '''Nueva funcionalidad, lista las ventas realizadas y muestra los totales de ventas por cantidad y valor
       Este método se diseño junto a la interfaz web para la entrega del proyecto 2
       Se deja habilitado para el rol Administrador y para los empleados 
    '''
    if current_user.tiene_habilitado_modulo('Heladeria.informe_ventas'):  
        productos_vendidos = Heladeria.traer_productos_vendidos()
        ventas_dias, valor_ventas_dias = Heladeria.totales_ventas()
        return render_template('informe_ventas.html', productos=productos_vendidos, ventas_dias=ventas_dias, valor_ventas_dias=valor_ventas_dias)    
    else:
        return redirect(url_for('login_bp.no_autorizado'))

@heladeria_blueprint.route('/listado_ingredientes')
@login_required
def listado_ingredientes():
    '''Equivale a Punto 5.8 Consultar todos los Ingredientes
       Este método se diseño junto a la interfaz web para la entrega del proyecto 2
       Se deja habilitado para el rol Administrador y para los empleados 
    '''
    if current_user.tiene_habilitado_modulo('Heladeria.listado_ingredientes'):      
        ingredientes = Ingrediente.traer_ingredientes()
        return render_template('listado_ingredientes.html', ingredientes=ingredientes)    
    else:
        return redirect(url_for('login_bp.no_autorizado'))
    
@heladeria_blueprint.route('/abastecer_ingrediente/<int:id>/')
@login_required
def abastecer_ingrediente(id:int):
    '''Equivale a Punto 5.12 Reabastecer un ingrediente según su ID
       Este método se diseño junto a la interfaz web para la entrega del proyecto 2
       Se deja habilitado para el rol Administrador y para los empleados 
    '''    
    if current_user.tiene_habilitado_modulo('Heladeria.abastecer_ingrediente'):      
        Ingrediente.abastecer_ingrediente(id)
        ingredientes = Ingrediente.traer_ingredientes()
        return render_template('listado_ingredientes.html', ingredientes=ingredientes)    
    else:
        return redirect(url_for('login_bp.no_autorizado'))
    
@heladeria_blueprint.route('/renovar_ingrediente/<int:id>/')
@login_required
def renovar_ingrediente(id:int):
    '''Equivale a Punto 5.13 Renovar el inventario de un ingrediente según su ID 
       Este método se diseño junto a la interfaz web para la entrega del proyecto 2
       Se deja habilitado para el rol Administrador y para los empleados 
    '''    
    if current_user.tiene_habilitado_modulo('Heladeria.renovar_ingrediente'):      
        Ingrediente.renovar_inventario(id)
        ingredientes = Ingrediente.traer_ingredientes()
        return render_template('listado_ingredientes.html', ingredientes=ingredientes)    
    else:
        return redirect(url_for('login_bp.no_autorizado'))
    
@heladeria_blueprint.route('/producto_mas_rentable')
@login_required
def producto_mas_rentable():
    '''Calcula el producto mas rentable dentro de los productos habilitados
       Este método se diseño junto a la interfaz web para la entrega del proyecto 2
       Se deja habilitado sólo para el rol Administrador
    '''
    if current_user.tiene_habilitado_modulo('Heladeria.producto_mas_rentable'):      
        producto_mas_rentable = Heladeria.calcular_producto_mas_rentable()
        return render_template('producto_mas_rentable.html', producto=producto_mas_rentable) 
    else:
        return redirect(url_for('login_bp.no_autorizado'))      
