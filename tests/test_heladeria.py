import unittest
from app import app, db, init_db
from models.producto import Producto
from models.producto_ingrediente import ProductoIngrediente
from models.heladeria_producto import HeladeriaProducto
from models.heladeria import Heladeria
from models.ingrediente import Ingrediente

class TestHeladeria(unittest.TestCase):

    def setUp(self):
        init_db(app)
        with app.app_context():
            producto_copa = Producto(id=21, nombre="Copa de Prueba", precio=30000.0\
                                        , tipo_vaso="", volumen= 300, id_tipo_producto = 1 )

            #relacioamos 2 ingredientes al producto
            producto_copa_ingredediente_1 = ProductoIngrediente(id_producto=21, id_ingrediente=1)
            producto_malteada_ingredediente_2 = ProductoIngrediente(id_producto=21, id_ingrediente=10)

            #agregar producto a la heladeria
            producto_copa_habilitar = HeladeriaProducto(id_heladeria=1, id_producto=21)

            db.session.add(producto_copa)
            db.session.add(producto_copa_ingredediente_1)
            db.session.add(producto_malteada_ingredediente_2)
            db.session.commit()    

            db.session.add(producto_copa_habilitar)
            db.session.commit()    

    def tearDown(self):
        with app.app_context():
            Producto.eliminar_por_id(21)           
            Ingrediente.abastecer_ingrediente(10) #Para que no quede en 0 el ingrediente al terminar la prueba

    def test_calcular_producto_mas_rentable(self):
        with app.app_context():
            producto_mas_rentable = Heladeria.calcular_producto_mas_rentable()
            #El producto ams rentable es el que se creo para la prueba
            self.assertEqual(producto_mas_rentable.nombre, "Copa de Prueba")            

    def test_vender_producto(self):
        with app.app_context():
            # Producto se puede vender
            self.assertEqual(Heladeria.vender_producto(21), "¡Vendido!" )

            #ahora renovamos el ingrediente 10 que es un complemento y hace parte del producto que se creo
            #con eso garantizamos que no se pueda vender
            #probamos que se genere una excepción
            Ingrediente.renovar_inventario(10)
            with self.assertRaises(ValueError) as exc:
               Heladeria.vender_producto(21)
            
            #print(str(exc.exception))
            #Probamos la exepción que se generó
            self.assertEqual(str(exc.exception), "Oh no! Nos hemos quedado sin Coco rallado" )
            
