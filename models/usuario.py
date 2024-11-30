from database.db import db
from flask_login import UserMixin
from models.rol import Rol

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuarios'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    ID_Rol = db.Column(db.Integer, db.ForeignKey('Roles.ID'),  nullable=False)
    
    rol = db.relationship('Rol', backref='Usuarios')        

    def __init__(self, user_id, username, password, id_rol):
        self.ID = user_id
        self.username = username
        self.password = password
        self.ID_Rol = id_rol

    def consultar_por_id(id_usuario):
        usuario = db.get_or_404(Usuario, id_usuario)
        return usuario     

    def consultar_por_nombre_password(username, password):
        #return db.session.execute(db.select(Perro).filter_by(Nombre=nombre)).scalars()
        return db.session.execute(\
                                  db.select(Usuario)
                                  .where(Usuario.username==username,
                                         Usuario.password==password)
                                  ).first()
               
    #Le decimos a flask cual es el Identificador de la table
    def get_id(self):
        return str(self.ID)
    
    # Flask-Login utiliza este atributo para saber si el usuario está activo
    @property
    def is_active(self):
        return True           