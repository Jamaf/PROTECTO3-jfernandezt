from models.heladeria import Heladeria
from models.producto import Producto
from models.ingrediente import Ingrediente

from flask import Blueprint
from flask import render_template

heladeria_blueprint = Blueprint('heladeria_bp', __name__, url_prefix="/")

@heladeria_blueprint.route('/') 
def index():
    productos_activos = Heladeria.traer_productos_habilitados()
    return render_template('index.html', productos=productos_activos)

@heladeria_blueprint.route('/gestion')
def gestion_home():
    return render_template('gestion.html')    

@heladeria_blueprint.route('/vender/<int:id>/')
def vender(id:int):
    resultado:str

    try:
        resultado = Heladeria.vender_producto(id)
        #print(f'Calorias { Producto.calcular_calorias(id)}')
        print(f'Costo Producción { Producto.calcular_costo(id)}')
        
    except ValueError as err:
        resultado = str(err)

    producto = Producto.consultar_por_id(id)

    return render_template('venta_detalle.html', resultado = resultado, producto=producto)    

@heladeria_blueprint.route('/informe_ventas')
def informe_ventas():
    productos_vendidos = Heladeria.traer_productos_vendidos()
    ventas_dias, valor_ventas_dias = Heladeria.totales_ventas()
    return render_template('informe_ventas.html', productos=productos_vendidos, ventas_dias=ventas_dias, valor_ventas_dias=valor_ventas_dias)    


@heladeria_blueprint.route('/listado_ingredientes')
def listado_ingredientes():
    ingredientes = Ingrediente.traer_ingredientes()
    return render_template('listado_ingredientes.html', ingredientes=ingredientes)    

@heladeria_blueprint.route('/abastecer_ingrediente/<int:id>/')
def abastecer_ingrediente(id:int):
    Ingrediente.abastecer_ingrediente(id)
    ingredientes = Ingrediente.traer_ingredientes()
    return render_template('listado_ingredientes.html', ingredientes=ingredientes)    

@heladeria_blueprint.route('/renovar_ingrediente/<int:id>/')
def renovar_ingrediente(id:int):
    Ingrediente.renovar_inventario(id)
    ingredientes = Ingrediente.traer_ingredientes()
    return render_template('listado_ingredientes.html', ingredientes=ingredientes)    

@heladeria_blueprint.route('/producto_mas_rentable')
def producto_mas_rentable():
    producto_mas_rentable = Heladeria.calcular_producto_mas_rentable()
    return render_template('producto_mas_rentable.html', producto=producto_mas_rentable)   
