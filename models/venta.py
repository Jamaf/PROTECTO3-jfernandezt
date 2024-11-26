from database.db import db
from sqlalchemy import text

class Venta(db.Model):
    __tablename__ = 'Ventas'

    id = db.Column(db.Integer, primary_key=True)
    id_heladeria = db.Column(db.SmallInteger, db.ForeignKey('Heladerias.id'), nullable=False)    
    id_cliente = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable=False)    
    id_producto = db.Column(db.SmallInteger, db.ForeignKey('Productos.id'), nullable=False)    
    cantidad_productos = db.Column(db.SmallInteger, nullable=False)
    valor_venta = db.Column(db.Numeric(8, 2), nullable=False)    
    fecha_venta = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), server_default=text('CURRENT_TIMESTAMP'), nullable=False)



        