from database.db import db
from database.db import ma
from models.tipo_ingrediente import TipoIngrediente

class Ingrediente(db.Model):
    __tablename__ = 'Ingredientes'

    id = db.Column(db.SmallInteger, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Numeric(8, 2), nullable=False)
    calorias = db.Column(db.Integer, nullable=True)
    inventario = db.Column(db.Numeric(8, 2), nullable=False)
    es_vegetariano = db.Column(db.Boolean, nullable=True)
    id_tipo_ingrediente = db.Column(db.SmallInteger, db.ForeignKey('Tipos_Ingredientes.id'), nullable=False)

    def traer_ingredientes():
        '''Consulta todos los ingredientes'''        
        return db.session.scalars(db.select(Ingrediente).order_by(Ingrediente.id)).all()    
    
    def abastecer_ingrediente(id_ingrediente):
        '''Para las ingredientes tipo Bases la función abastecer sumará 5 en el inventario, mientras que para los Complementos se aumentará en 10'''
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)
        
        #Si el ingrediente es Base
        if ingrediente.id_tipo_ingrediente == 1:
            ingrediente.inventario += 5
        else:
            ingrediente.inventario += 10

        ingrediente.verified = True

        db.session.commit()       

        return 

    def renovar_inventario(id_ingrediente):
        '''Renueva el inventario de un ingrediente de tipo Complemento'''
        ingrediente = Ingrediente.consultar_por_id(id_ingrediente)

        if ingrediente.id_tipo_ingrediente == 1:
            raise ValueError('Solo se renuevan los complementos')
        
        # Solo se renueva para los complementos
        db.session.execute(db.update(Ingrediente)
                                    .where(Ingrediente.id == id_ingrediente,
                                           Ingrediente.id_tipo_ingrediente == 2)
                                    .values(inventario = 0.0))
        db.session.commit()
        return 
        

    def es_sano(id_ingrediente):    
        '''Un ingrediente es sano si tiene estricatamente menos de 100 calorias o si es vegetariano'''
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)

        return True if ingrediente.calorias < 100 or ingrediente.es_vegetariano == True else False

    def eliminar_por_id(id_ingrediente):
        '''Elimina un ingrediente a través de su id'''
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)
        db.session.delete(ingrediente)
        db.session.commit()
        return 
    
    def consultar_por_id(id_ingrediente):
        '''Consulta un ingrediente a través de su id'''
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)
        return ingrediente    
    
    def consultar_por_nombre(nombre):
        '''Consulta un ingrediente a través de su nombre'''
        return db.session.scalars(db.select(Ingrediente).where(Ingrediente.nombre==nombre)).first()
        
class IngredienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingrediente
        include_fk = True