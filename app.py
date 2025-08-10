from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app, supports_credentials=True)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzadb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Initialize DB with sample data
with app.app_context():
    db.create_all()
    if MenuItem.query.count() == 0:
        sample_menu = [
            MenuItem(name="Margherita", price=199),
            MenuItem(name="Farmhouse", price=299),
            MenuItem(name="Peppy Paneer", price=329),
            MenuItem(name="Cheese n Corn", price=249),
            MenuItem(name="Veggie Paradise", price=279),
            MenuItem(name="Capsicum & Red Paprika", price=89),
            MenuItem(name="extravaganza", price=219),
            MenuItem(name="Veg Barbeque ", price=239)
        ]
        db.session.add_all(sample_menu)
        db.session.commit()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 409
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})

@app.route("/api/menu", methods=["GET"])
def get_menu():
    items = MenuItem.query.all()
    return jsonify([{ "id": i.id, "name": i.name, "price": i.price } for i in items])

@app.route("/api/cart", methods=["GET", "POST", "DELETE"])
def cart():
    if 'cart' not in session:
        session['cart'] = []

    if request.method == 'GET':
        return jsonify(session['cart'])

    elif request.method == 'POST':
        data = request.get_json()
        cart = session['cart']
        for item in cart:
            if item['item'] == data['item']:
                item['qty'] += data.get('qty', 1)
                session['cart'] = cart
                return jsonify({"message": "Quantity updated"})
        cart.append({"item": data['item'], "price": data['price'], "qty": data.get('qty', 1)})
        session['cart'] = cart
        return jsonify({"message": "Item added to cart"})

    elif request.method == 'DELETE':
        session['cart'] = []
        return jsonify({"message": "Cart cleared"})

@app.route("/api/checkout", methods=["POST"])
def checkout():
    session['cart'] = []
    return jsonify({"message": "Order placed successfully"})

if __name__ == '__main__':
    app.run(debug=True)
