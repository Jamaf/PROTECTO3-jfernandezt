from database.db import db

class HeladeriaProducto(db.Model):
    __tablename__ = 'Heladerias_Productos'

    id = db.Column(db.SmallInteger, primary_key=True)
    id_heladeria = db.Column(db.SmallInteger, db.ForeignKey('Heladerias.id'), nullable=False)    
    id_producto = db.Column(db.SmallInteger, db.ForeignKey('Productos.id'), nullable=False)    
    __table_args__ = (db.UniqueConstraint("id_heladeria", "id_producto", name="UIX_Heladerias_Productos"), )