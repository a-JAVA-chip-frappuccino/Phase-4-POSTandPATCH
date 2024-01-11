from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    serialize_rules = ('-foods_at_restaurant.restaurant', )

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

    foods_at_restaurant = db.relationship('FoodAtRestaurant', back_populates = 'restaurant', cascade = 'all,delete')

    # validation of name column for restaurants table
    @validates("name")
    def validate_name(self, key, value):
        if len(value) >= 25:
            raise ValueError # raises error if inputted name is too long
        else:
            return value

class Food(db.Model, SerializerMixin):
    __tablename__ = "foods"

    serialize_rules = ('-restaurants_with_food.food', )

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

    restaurants_with_food = db.relationship('FoodAtRestaurant', back_populates = 'food', cascade = 'all,delete')

class FoodAtRestaurant(db.Model, SerializerMixin):
    __tablename__ = "food_at_restaurant"

    serialize_rules = ('-restaurant.foods_at_restaurant', '-food.restaurants_with_food')

    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Float)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    food_id = db.Column(db.Integer, db.ForeignKey("foods.id"))

    restaurant = db.relationship('Restaurant', back_populates = 'foods_at_restaurant')
    food = db.relationship('Food', back_populates = 'restaurants_with_food')

    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError
        else:
            return value