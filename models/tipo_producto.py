from database.db import db

class TipoProducto(db.Model):
    __tablename__ = 'Tipos_Productos'

    id = db.Column(db.SmallInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)