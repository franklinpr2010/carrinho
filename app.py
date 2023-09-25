from flask import Flask
from routes import carrinho_blueprint
from models import db, init_app
from flask_migrate import Migrate
import os
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = "pSaOCtBJ90oNkW9nigTXAw"
db_path = os.path.join(os.path.dirname(__file__), 'database/carrinho.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(carrinho_blueprint)
init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)