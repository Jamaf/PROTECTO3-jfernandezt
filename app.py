from flask import Flask
from flask import render_template
from dotenv import load_dotenv
import os

from database.db import db
from database.db import init_db

from controllers.ingrediente_controller import ingrediente_blueprint
from controllers.producto_controller import producto_blueprint
from controllers.heladeria_controller import heladeria_blueprint

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

#Aqui configuro la app para el objeto db
db.init_app(app)
init_db(app)

app.register_blueprint(ingrediente_blueprint)
app.register_blueprint(producto_blueprint)
app.register_blueprint(heladeria_blueprint)

#@app.route('/') 
#def index():
#    return "Hola Mundo"#render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)