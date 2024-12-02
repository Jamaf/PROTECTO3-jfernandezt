from database.db import db
from sqlalchemy import select, join, update
from sqlalchemy.sql.functions import func

from models.producto import Producto
from models.cliente import Cliente
from models.venta import Venta
from models.ingrediente import Ingrediente
from models.producto_ingrediente import ProductoIngrediente
from models.heladeria_producto import HeladeriaProducto

class Heladeria(db.Model):
    __tablename__ = 'Heladerias'

    id = db.Column(db.SmallInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def traer_todos():
        '''Consulta las heladerias'''        
        return db.session.scalars(db.select(Heladeria).order_by(Heladeria.id)).all()
    
    def traer_productos_habilitados():
        '''Consulta todos los productos habilitados para la Heladeria'''
        stmt = (
            select(Producto.id, Producto.nombre, Producto.precio, Producto.volumen)
            .select_from(join(Producto, HeladeriaProducto, Producto.id == HeladeriaProducto.id_producto)
                        )
        )
        return db.session.execute(stmt).all()

    def traer_productos_vendidos():
        '''Consulta todos los productos vendidos'''
        stmt = (
            select(Producto.id, Producto.nombre, Producto.precio, Venta.cantidad_productos)
            .select_from(join(Producto, Venta, Producto.id == Venta.id_producto)
                        )
        )
        return db.session.execute(stmt).all()
    
    def totales_ventas():
        '''Resumen de las ventas realizadas por días y por valor'''
        stmt =  (select(func.count(Venta.id).label('ventas_dias'), func.sum(Producto.precio).label('valor_ventas_dias'))
                    .select_from(join(Producto, Venta, Producto.id == Venta.id_producto))
        )
        result = db.session.execute(stmt).all()

        return(result[0].ventas_dias, result[0].valor_ventas_dias)


    def calcular_producto_mas_rentable():
        '''Calcula el producto mas rentble'''
        productos_habilitados = Heladeria.traer_productos_habilitados()

        producto_mas_rentable = None
        valor_producto_mas_rentable = 0.0

        for producto in productos_habilitados:
            #print(type(producto))
            rentabilidad = Producto.calcular_rentabilidad(producto.id)
            if rentabilidad > valor_producto_mas_rentable:
                producto_mas_rentable = producto
                valor_producto_mas_rentable = rentabilidad
        
        return producto_mas_rentable
            

    def vender_producto(id_producto):
        '''Funcionalidad que permite vender un producto
           Esta funcionalidad es usada por la heladeria WEB y la API 
        '''

        #Consulta para obtener el primer ingrediente Base (id_tipo_ingrediente es 1) con insuficiencia de inventario
        stmt = (
                    select(Ingrediente.nombre)
                        .select_from(join(ProductoIngrediente, Ingrediente, Ingrediente.id == ProductoIngrediente.id_ingrediente)
                                    )
                        .where(ProductoIngrediente.id_producto == id_producto,
                               Ingrediente.id_tipo_ingrediente == 1,
                               Ingrediente.inventario < 0.2)
                )
        cant_bases_insuficientes = db.session.execute(stmt).first()

        if cant_bases_insuficientes is not None:
            raise ValueError(f'Oh no! Nos hemos quedado sin {cant_bases_insuficientes[0]}')

        #Consulta para obtener el primer ingrediente Complemento (id_tipo_ingrediente es 2) con insuficiencia de inventario
        stmt = (
                    select(Ingrediente.nombre)
                        .select_from(join(ProductoIngrediente, Ingrediente, Ingrediente.id == ProductoIngrediente.id_ingrediente)
                                    )
                        .where(ProductoIngrediente.id_producto == id_producto,
                               Ingrediente.id_tipo_ingrediente == 2,
                               Ingrediente.inventario < 1.0)
                )
        cant_complementos_insuficientes = db.session.execute(stmt).first() 

        if cant_complementos_insuficientes is not None:
            raise ValueError(f'Oh no! Nos hemos quedado sin {cant_complementos_insuficientes[0]}')        

        #si llega hasta aca indica que hay los ingredientes necesarios para vender el producto
        #actualizamos las bases descontando del inventario
        stmt = (
                    update(Ingrediente)
                        .where(Ingrediente.id == ProductoIngrediente.id_ingrediente,
                               ProductoIngrediente.id_producto == id_producto,
                               Ingrediente.id_tipo_ingrediente == 1)
                        .values(inventario = Ingrediente.inventario - 0.2)
                )
        db.session.execute(stmt)

        #actualizamos los complementos descontando del inventario
        stmt = (
                    update(Ingrediente)
                        .where(Ingrediente.id == ProductoIngrediente.id_ingrediente,
                               ProductoIngrediente.id_producto == id_producto,
                               Ingrediente.id_tipo_ingrediente == 2)
                        .values(inventario = Ingrediente.inventario - 1)
                )
        db.session.execute(stmt)        

        producto = Producto.consultar_por_id(id_producto)

        # INgresamos una nueva venta, se dejan datos dummy para cliente y cantidad de productos
        nueva_venta = Venta(id_heladeria= 1, id_cliente = 1, id_producto = id_producto, valor_venta =producto.precio, cantidad_productos = 1)
        db.session.add(nueva_venta)

        db.session.commit()

        return "¡Vendido!"  
