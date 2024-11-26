from database.db import db

class ProductoIngrediente(db.Model):
    __tablename__ = 'Productos_Ingredientes'

    id = db.Column(db.SmallInteger, primary_key=True)
    id_producto = db.Column(db.SmallInteger, db.ForeignKey('Productos.id'), nullable=False)    
    id_ingrediente = db.Column(db.SmallInteger, db.ForeignKey('Ingredientes.id'), nullable=False)    
    __table_args__ = (db.UniqueConstraint("id_producto", "id_ingrediente", name="UIX_Productos_Ingredientes"), )