from config import app
from flask import make_response, request
from flask_restful import Api, Resource

from models import db, Restaurant, Food, FoodAtRestaurant

api = Api(app)

# POST request to restaurants table
@app.route('/restaurants', methods = ['POST'])
def restaurants():
    # try block runs until ValueError is raised,
    # in which case code switches to except block
    try:
        form_data = request.get_json() # grabs information sent back from frontend

        # creates new instance
        new_restaurant = Restaurant(
            name = form_data['name']
        )

        # adds and commits instance as row to DB
        db.session.add(new_restaurant)
        db.session.commit()

        response = make_response(
            new_restaurant.to_dict(),
            201
        )
    except ValueError:
        response = make_response(
            {"Error" : "ValueError raised during creation!"},
            400
        )

    return response

# PATCH request to food_at_restaurant table
@app.route('/food_at_restaurants/<int:id>', methods = ['PATCH'])
def food_at_restaurant_by_id(id):
    rf = FoodAtRestaurant.query.filter(FoodAtRestaurant.id == id).first()

    if rf:
        try:
            form_data = request.get_json()

            # updates in table each column of row such that it matches incoming key:value pair
            for attr in form_data:
                setattr(rf, attr, form_data[attr])

            # commits changes of instance to DB
            db.session.commit()

            response = make_response(
                rf.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                {"Error" : "ValueError raised during creation!"},
                400
            )
    else:
        response = make_response(
            {"Error" : "FoodAtRestaurant object does not exist!"},
            404
        )

    return response

# POST request to food_at_restaurant table
class FoodsAtRestaurants(Resource):
    def post(self):
        try:
            form_data = request.get_json()

            new_food_at_restaurant = FoodAtRestaurant(
                price = form_data['price'],
                restaurant_id = form_data['restaurant_id'],
                food_id = form_data['food_id']
            )

            db.session.add(new_food_at_restaurant)
            db.session.commit()

            response = make_response(
                new_food_at_restaurant.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                {"Error" : "ValueError raised during creation!"},
                400
            )

        return response
    
api.add_resource(FoodsAtRestaurants, '/food_at_restaurants')

if __name__ == '__main__':
    app.run(port = 5555, debug = True)