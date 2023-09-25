from flask import Blueprint, jsonify, request
import requests
from models import Carrinho, CarrinhoItem, db



carrinho_blueprint = Blueprint('carrinho_api_routes', __name__, url_prefix="/api/carrinho")

USER_API_URL = 'http://user-store:5001/api/user'

def get_user(api_key):
    headers = {
        'Authorization': api_key
    }
    response = requests.get(USER_API_URL, headers=headers)
    respon_json = response.json()
    print(respon_json)
    if respon_json['status'] != '200':
        return {'message': 'Not Authorized'}
    user = response.json()
    return user


@carrinho_blueprint.route('/', methods=['GET'])
def get_open_carrinho():
    api_key = request.headers.get('Authorization')
    print(api_key)
    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401
    response = get_user(api_key)
    print(response)
    user = response.get('result')
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    open_carrinho = Carrinho.query.filter_by(user_id=user['id'], is_open=1).first()
    if open_carrinho:
        return jsonify({
            'result': open_carrinho.serialize()
        })
    else:
        return jsonify({'message': 'Nenhum carrinho aberto'})
    



@carrinho_blueprint.route('/all', methods=['GET'])
def all_carrinhos():
    carrinhos = Carrinho.query.all()
    result = [carrinho.serialize() for carrinho in carrinhos]
    return jsonify(result), 200



@carrinho_blueprint.route('/add-item', methods=['POST'])
def add_carrinho_item():
    api_key = request.headers.get('Authorization')
    print(api_key)
    if not api_key:
        return jsonify({'message': 'Usuário não logado'}), 401
    response = get_user(api_key)
    print(response)
    if not response.get('result'):
        return jsonify({'message': 'Usuário não logado'}), 401
    user = response.get('result')
    produto_id = int(request.form['produto_id'])
    quantity = int(request.form['quantity'])
    user_id = user['id']
    open_carrinho = Carrinho.query.filter_by(user_id=user_id, is_open=1).first()

    if not open_carrinho:
        open_carrinho = Carrinho()
        open_carrinho.is_open = True
        open_carrinho.user_id = user_id
        carrinho_item = CarrinhoItem(produto_id=produto_id, quantity=quantity)
        open_carrinho.carrinho_items.append(carrinho_item)
    else:
        found = False
        for item in open_carrinho.carrinho_items:
            if item.produto_id == produto_id:
                item.quantity += quantity
                found = True
        if not found:
            carrinho_item = CarrinhoItem(book_id=produto_id, quantity=quantity)
            open_carrinho.carrinho_items.append(carrinho_item)
    db.session.add(open_carrinho)
    db.session.commit()
    return jsonify({"result": open_carrinho.serialize()})



@carrinho_blueprint.route('/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    open_carrinho = Carrinho.query.filter_by(user_id=user['id'], is_open=1).first()
    if open_carrinho:
        open_carrinho.is_open = False
        db.session.add(open_carrinho)
        db.session.commit()
        return jsonify({'result': open_carrinho.serialize()})
    else:
        return jsonify({'message': 'Nenhum carrinho aberto!!!!!!!'})
