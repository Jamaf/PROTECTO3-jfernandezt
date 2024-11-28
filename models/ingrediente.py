from database.db import db, ma

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
        return db.session.scalars(db.select(Ingrediente).order_by(Ingrediente.id)).all()    
    
    def abastecer_ingrediente(id_ingrediente):
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
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)

        return True if ingrediente.calorias < 100 or ingrediente.es_vegetariano == True else False

    def eliminar_por_id(id_ingrediente):
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)
        db.session.delete(ingrediente)
        db.session.commit()
        return 
    
    def consultar_por_id(id_ingrediente):
        ingrediente = db.get_or_404(Ingrediente, id_ingrediente)
        return ingrediente    
    
    def consultar_por_nombre(nombre):
        return db.session.scalars(db.select(Ingrediente).where(Ingrediente.nombre==nombre)).first()
        
class IngredienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingrediente
        include_fk = True