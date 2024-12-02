from database.db import db
from flask_login import UserMixin
from models.rol import Rol

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    id_rol = db.Column(db.SmallInteger, db.ForeignKey('Roles.id'),  nullable=False)
    
    #permite obtener el rol del usuario como si fuese un campo más
    rol = db.relationship('Rol', backref='Usuarios')        

    def __init__(self, user_id, username, password, id_rol):
        self.id = user_id
        self.username = username
        self.password = password
        self.id_rol = id_rol

    def consultar_por_id(id_usuario):
        '''Se busca un usuario por su id'''
        usuario = db.get_or_404(Usuario, id_usuario)
        return usuario     

    def consultar_por_nombre_password(username, password):
        '''
        Consulta un usuaio por nombre y password

        Parameters:
            username: username del usuario a validar
            password: password del usuario

        Returns:
            Usuario cuando se encuentra, None en caso contario
        '''   
        return db.session.execute(\
                                  db.select(Usuario)
                                  .where(Usuario.username==username,
                                         Usuario.password==password)
                                  ).first()

    def tiene_habilitado_modulo(self, nombre_modulo):
        '''
        Valida si el Usurio(Rol) tiene habilitado el módulo

        Parameters:
            nombre_modulo: Nombre del modulo a validar

        Returns:
            True: si el módulo esta habilitado para el Rol, False de lo contrario
        '''     
        #Se usa list comprehension para armar una lista con los nombre de los módulos del rol     
        if nombre_modulo in [rm.modulo.nombre for rm in self.rol.rol_modulo]:
            return True
        return False        

    def get_id(self):
        '''Le decimos a flask cual es el Identificador de la tabla'''
        return str(self.id)
    
    # Flask-Login utiliza este atributo para saber si el usuario está activo
    @property
    def is_active(self):
        return True           