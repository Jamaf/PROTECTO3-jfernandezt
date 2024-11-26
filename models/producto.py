from database.db import db
from sqlalchemy import select, join, update
from sqlalchemy.sql.functions import func

from models.ingrediente import Ingrediente
from models.producto_ingrediente import ProductoIngrediente
from models.heladeria_producto import HeladeriaProducto
from models.venta import Venta

class Producto(db.Model):
    __tablename__ = 'Productos'

    id = db.Column(db.SmallInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Numeric(8, 2), nullable=False)
    tipo_vaso = db.Column(db.String(50), nullable=True)
    volumen = db.Column(db.Integer, nullable=True)
    id_tipo_producto = db.Column(db.SmallInteger, db.ForeignKey('Tipos_Productos.id'), nullable=False)

    def traer_todos():
        return db.session.scalars(db.select(Producto).order_by(Producto.id)).all()
        
    def consultar_por_id(id_producto):
        producto = db.get_or_404(Producto, id_producto)
        return producto

    #Primera versión de verificar existencias
    def verificar_existencias(id_producto):
        #Consulta para validar la existencia del tipo de ingrediente Base (id_tipo_ingrediente es 1)
        stmt = (
                    select(func.count(ProductoIngrediente.id_producto))
                        .select_from(join(ProductoIngrediente, Ingrediente, Ingrediente.id == ProductoIngrediente.id_ingrediente)
                                    )
                        .where(ProductoIngrediente.id_producto == id_producto,
                               Ingrediente.id_tipo_ingrediente == 1,
                               Ingrediente.inventario < 0.2)
                )
        cant_bases_insuficientes = db.session.execute(stmt).scalar()  

        #Consulta para validar la existencia del tipo de ingrediente Complemento (id_tipo_ingrediente es 2)
        stmt = (
                    select(func.count(ProductoIngrediente.id_producto))
                        .select_from(join(ProductoIngrediente, Ingrediente, Ingrediente.id == ProductoIngrediente.id_ingrediente)
                                    )
                        .where(ProductoIngrediente.id_producto == id_producto,
                               Ingrediente.id_tipo_ingrediente == 2,
                               Ingrediente.inventario < 1.0)
                )
        cant_complementos_insuficientes = db.session.execute(stmt).scalar()  
        

        # Ejecutar la consulta
        return True if cant_bases_insuficientes == 0 and cant_complementos_insuficientes == 0 else False   
    

    def calcular_rentabilidad(id_producto):
        '''
        Calcula la la rentabilidad de un producto como la diferencia entre el precio de
        venta del producto, y el costo de sus ingredientes

        Parameters:
            id_producto: Id del produto a validar

        Returns:
            float: rentabilidad calculada, precio - costo de ingredientes 
        '''    
        costo_ingredientes = Producto.calcular_costo(id_producto)

        producto = Producto.consultar_por_id(id_producto)

        return producto.precio - costo_ingredientes
    

    def calcular_calorias(id_producto): 
        '''
        Permita hacer el conteo de calorías de un producto redondeado a 2 cifras.

        Parameters:
            id_producto: Id del produto a validar

        Returns:
            float: suma de las calorias de los ingredientes
        '''            
        stmt = (
                    select(func.sum(Ingrediente.calorias))
                        .select_from(join(ProductoIngrediente, Ingrediente, Ingrediente.id == ProductoIngrediente.id_ingrediente)
                                    )
                        .where(ProductoIngrediente.id_producto == id_producto)
                )
        calorias_calculadas = db.session.execute(stmt).scalar()

        producto = Producto.consultar_por_id(id_producto)

        #si el producto es Copa == 1
        if producto.id_tipo_producto == 1:
            calorias_calculadas *= 0.95
        else:
            calorias_calculadas += 200

        return round(calorias_calculadas, 2)

    def calcular_costo(id_producto): 
        '''
        Calcula el costo de un producto a partir de los ingredientes
        Para las malteadas se sumarán 500 pesos por el uso de vasos plásticos.

        Parameters:
            id_producto: Id del produto a validar
        
        Returns:
            float: suma del costo de los ingredientes para hacer una copa o una malteada
        '''              
        stmt = (
                    select(func.sum(Ingrediente.precio))
                        .select_from(join(ProductoIngrediente, Ingrediente, Ingrediente.id == ProductoIngrediente.id_ingrediente)
                                    )
                        .where(ProductoIngrediente.id_producto == id_producto)
                )
        costo_ingredientes = db.session.execute(stmt).scalar()

        producto = Producto.consultar_por_id(id_producto)

        #si el producto es Malteada se suman 500
        if producto.id_tipo_producto == 2:
            costo_ingredientes += 500

        return costo_ingredientes

    def eliminar_por_id(id_producto):

        stmt = (
            db.delete(ProductoIngrediente)
                .where(ProductoIngrediente.id_producto == id_producto)
        )
        db.session.execute(stmt)

        stmt = (
            db.delete(HeladeriaProducto)
                .where(HeladeriaProducto.id_producto == id_producto)
        )
        db.session.execute(stmt)

        stmt = (
            db.delete(Venta)
                .where(Venta.id_producto == id_producto)
        )
        db.session.execute(stmt)

        producto = db.get_or_404(Producto, id_producto)
        db.session.delete(producto)
        db.session.commit()
        return 
    