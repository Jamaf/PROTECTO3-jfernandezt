import unittest
from app import app, db, init_db
from models.producto import Producto
from models.producto_ingrediente import ProductoIngrediente

class TestIngrediente(unittest.TestCase):
    def setUp(self):
        init_db(app)
        with app.app_context():
            producto_copa = Producto(id=21, nombre="Copa de Prueba", precio=30000.0\
                                        , tipo_vaso="", volumen= 300, id_tipo_producto = 1 )
            producto_malteada = Producto(id=22, nombre="Malteada de Prueba", precio=30000.0\
                                        , tipo_vaso="", volumen= 300, id_tipo_producto = 2 )

            producto_copa_ingredediente_1 = ProductoIngrediente(id_producto=21, id_ingrediente=1)
            producto_copa_ingredediente_2 = ProductoIngrediente(id_producto=21, id_ingrediente=2)

            producto_malteada_ingredediente_1 = ProductoIngrediente(id_producto=22, id_ingrediente=3)
            producto_malteada_ingredediente_2 = ProductoIngrediente(id_producto=22, id_ingrediente=4)            

            db.session.add(producto_copa)
            db.session.add(producto_malteada)

            db.session.add(producto_copa_ingredediente_1)
            db.session.add(producto_copa_ingredediente_2)

            db.session.add(producto_malteada_ingredediente_1)
            db.session.add(producto_malteada_ingredediente_2)

            db.session.commit()    

    def tearDown(self):
        with app.app_context():
            Producto.eliminar_por_id(21)           
            Producto.eliminar_por_id(22)  

    def test_abastecer_ingrediente(self):
        with app.app_context():
            producto_copa_calorias = Producto.calcular_calorias(21)
            producto_malteada_calorias = Producto.calcular_calorias(22)

            self.assertEqual(producto_copa_calorias, 460 * 0.95 )
            self.assertEqual(producto_malteada_calorias, 215 + 200)        

    def test_calcular_costo(self):
        with app.app_context():
            producto_copa_costo = Producto.calcular_costo(21)
            producto_malteada_costo = Producto.calcular_costo(22)

            self.assertEqual(producto_copa_costo, 2300.00 )
            self.assertEqual(producto_malteada_costo, 5500.00 + 500.00)        

    def test_calcular_rentabilidad(self):
        with app.app_context():
            producto_copa_rentabilidad = Producto.calcular_rentabilidad(21)
            producto_malteada_rentabilidad = Producto.calcular_rentabilidad(22)

            self.assertEqual(producto_copa_rentabilidad, 27700.00 )
            self.assertEqual(producto_malteada_rentabilidad, 24000.00)         
     
    