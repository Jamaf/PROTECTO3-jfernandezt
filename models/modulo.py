from database.db import db

class Modulo(db.Model):
    __tablename__ = 'Modulos'
    id = db.Column(db.SmallInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)