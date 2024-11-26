from database.db import db

class Cliente(db.Model):
    __tablename__ = 'Clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def traer_todos():
        return db.session.scalars(db.select(Cliente).order_by(Cliente.id)).all()