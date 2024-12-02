from database.db import db
from models.modulo import Modulo

class RolModulo(db.Model):
    __tablename__ = 'Roles_Modulos'

    id = db.Column(db.SmallInteger, primary_key=True)
    id_rol = db.Column(db.SmallInteger, db.ForeignKey('Roles.id'), nullable=False)    
    id_modulo = db.Column(db.SmallInteger, db.ForeignKey('Modulos.id'), nullable=False)    
    __table_args__ = (db.UniqueConstraint("id_rol", "id_modulo", name="UIX_Roles_Modulos"), )

    modulo = db.relationship('Modulo', backref='Modulos')