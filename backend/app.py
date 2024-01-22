# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy=True)

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    restaurants = db.relationship('RestaurantPizza', backref='pizza', lazy=True)

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Schema for Marshmallow
class RestaurantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Restaurant

    id = ma.auto_field()
    name = ma.auto_field()
    pizzas = ma.Nested('PizzaSchema', many=True)

class PizzaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pizza

    id = ma.auto_field()
    name = ma.auto_field()
    restaurants = ma.Nested('RestaurantSchema', many=True)

class RestaurantPizzaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RestaurantPizza

    id = ma.auto_field()
    restaurant_id = ma.auto_field()
    pizza_id = ma.auto_field()
    price = ma.auto_field()

# Schemas instances
restaurant_schema = RestaurantSchema()
pizza_schema = PizzaSchema()
restaurant_pizza_schema = RestaurantPizzaSchema()

# Routes
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify(restaurant_schema.dump(restaurants, many=True))

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify(pizza_schema.dump(pizzas, many=True))

@app.route('/restaurant_pizzas', methods=['GET'])
def get_restaurant_pizzas():
    restaurant_pizzas = RestaurantPizza.query.all()
    return jsonify(restaurant_pizza_schema.dump(restaurant_pizzas, many=True))

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json

    # Validate input data
    if not (1 <= data['price'] <= 30):
        return jsonify({'error': 'Invalid price. Must be between 1 and 30.'}), 400

    new_pizza = RestaurantPizza(
        restaurant_id=data['restaurant_id'],
        pizza_id=data['pizza_id'],
        price=data['price']
    )
    db.session.add(new_pizza)
    db.session.commit()
    return jsonify(restaurant_pizza_schema.dump(new_pizza)), 201 
@app.route('/restaurant_pizzas/<int:rp_id>', methods=['PUT'])
def update_restaurant_pizza(rp_id):
    data = request.json

    restaurant_pizza = RestaurantPizza.query.get_or_404(rp_id)
    restaurant_pizza.price = data['price']

    db.session.commit()

    return jsonify(restaurant_pizza_schema.dump(restaurant_pizza))

@app.route('/restaurant_pizzas/<int:rp_id>', methods=['DELETE'])
def delete_restaurant_pizza(rp_id):
    restaurant_pizza = RestaurantPizza.query.get_or_404(rp_id)

    db.session.delete(restaurant_pizza)
    db.session.commit()

    return jsonify({'message': 'RestaurantPizza deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)