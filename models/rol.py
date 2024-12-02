from database.db import db
from models.rol_modulo import RolModulo
class Rol(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.SmallInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    rol_modulo = db.relationship('RolModulo', backref='Roles_Modulos')