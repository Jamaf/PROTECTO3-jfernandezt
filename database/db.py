from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#db = SQLAlchemy(app)
#Lo vamos a inciair sin app
#luego en el app.py se le configura
db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        #db.drop_all() #Si se quiere borrar las tablas de la BD
        db.create_all()

ma = Marshmallow()        
