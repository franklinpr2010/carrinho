from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_open = db.Column(db.Boolean, default=False)
    carrinho_items = db.relationship('CarrinhoItem', backref="carrinhoItem")

    def serialize(self):
        return {
            'user_id': self.user_id,
            'is_open': self.is_open,
            'carrinho_items': [x.serialize() for x in self.carrinho_items]
        }


class CarrinhoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinho.id'))
    produto_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, produto_id, quantity):
        self.produto_id = produto_id
        self.quantity = quantity

    def serialize(self):
        return {
            'produto': self.produto_id,
            'quantity': self.quantity
        }
