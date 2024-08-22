from flask import Flask, request, jsonify
from models import db, Order
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

def get_user(user_id):
    response = requests.get(f'http://users_service:5002/users/{user_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_book(book_id):
    response = requests.get(f'http://books_service:5001/books/{book_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user = get_user(data['user_id'])
    book = get_book(data['book_id'])
    
    if not user or not book:
        return jsonify({'message': 'User or Book not found'}), 404
    
    new_order = Order(user_id=data['user_id'], book_id=data['book_id'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        user = get_user(order.user_id)
        book = get_book(order.book_id)
        if user and book:
            order_info = {
                'id': order.id,
                'user': user,
                'book': book
            }
            orders_list.append(order_info)
    return jsonify(orders_list)

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    orders_list = []
    for order in orders:
        user = get_user(order.user_id)
        book = get_book(order.book_id)
        if user and book:
            order_info = {
                'id': order.id,
                'user': user,
                'book': book
            }
            orders_list.append(order_info)
    return jsonify(orders_list)

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
