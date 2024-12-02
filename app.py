from flask import Flask
from dotenv import load_dotenv
import os

from database.db import db
from database.db import ma
from database.db import login_manager
from database.db import init_db

from controllers.ingrediente_controller import ingrediente_blueprint
from controllers.producto_controller import producto_blueprint
from controllers.heladeria_controller import heladeria_blueprint
from controllers.login_controller import login_blueprint

#Cargar las variables ocultas
load_dotenv()

app = Flask(__name__, template_folder="views")

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Por buena practica

SECRET_KEY = os.urandom(24)
app.config["SECRET_KEY"] = SECRET_KEY

#Configuro BD, marshmallow y login manager
db.init_app(app)
init_db(app)
ma.init_app(app)
login_manager.init_app(app)

app.register_blueprint(ingrediente_blueprint)
app.register_blueprint(producto_blueprint)
app.register_blueprint(heladeria_blueprint)
app.register_blueprint(login_blueprint)


if __name__ == '__main__':
    app.run(debug=True)