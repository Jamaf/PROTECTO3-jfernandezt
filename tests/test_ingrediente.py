import unittest
from app import app, db, init_db
from models.ingrediente import Ingrediente

class TestIngrediente(unittest.TestCase):
    def setUp(self):
        init_db(app)
        with app.app_context():
            ingrediente_base = Ingrediente(id=21, nombre="Ingrediente de Prueba", precio=2350.0\
                                        , calorias=200, inventario=10.0, es_vegetariano=False, id_tipo_ingrediente = 1 )
            ingrediente_complemento = Ingrediente(id=22, nombre="Ingrediente vegetariano ", precio=2350.0\
                                        , calorias=200, inventario=10.0, es_vegetariano=True, id_tipo_ingrediente = 2 )          
            db.session.add(ingrediente_base)
            db.session.add(ingrediente_complemento)
            db.session.commit()    

    def tearDown(self):
        with app.app_context():
            Ingrediente.eliminar_por_id(21)           
            Ingrediente.eliminar_por_id(22)  
    
    def test_es_sano(self):
        with app.app_context():
            self.assertEqual(Ingrediente.es_sano(21), False)
            self.assertEqual(Ingrediente.es_sano(22), True)

    def test_abastecer_ingrediente(self):
        with app.app_context():
            Ingrediente.abastecer_ingrediente(21)
            Ingrediente.abastecer_ingrediente(22)

            #los ingredientes se abastecen en 5 o 10 de acuerdo a si es Base o Complemento
            #al momento de crearse se definió su inventario en 10 para los dos ingredientes
            ingrediente_1_abastecido = Ingrediente.consultar_por_id(21)
            ingrediente_2_abastecido = Ingrediente.consultar_por_id(22)

            self.assertEqual(ingrediente_1_abastecido.inventario, 15.00)
            self.assertEqual(ingrediente_2_abastecido.inventario, 20.00)
            
    def test_renovar_inventario(self):
        with app.app_context():
            #El proceso de renovacion solo aplica para los Complementos
            Ingrediente.renovar_inventario(22)
            ingrediente_2_renovado = Ingrediente.consultar_por_id(22)
            self.assertEqual(ingrediente_2_renovado.inventario, 0.00)

            #Cuando el ingrediente NO es un Complemeto se genera una excepcion
            with self.assertRaises(ValueError):
                Ingrediente.renovar_inventario(21)
