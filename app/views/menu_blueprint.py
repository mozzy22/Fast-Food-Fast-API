from app.models.db_user_sql_queries import UserQueries
from app.models.orders import Orders
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from app.views.user_blueprint import token_required

My_blue = Blueprint('menu', __name__ )
#from routes import order_obj
order_obj = Orders()
querry = UserQueries()

#A function for admin to add food items to the menu
@My_blue.route('/api/v1/menu', methods=['POST'])
@token_required
@swag_from('../docs/add_menu.yml')
def add_food_items(current_user):
    "A function that adds food items"
    if not querry.check_admin(current_user):
        return jsonify({"error" : "only admin alowed"}), 401
    new_food = request.json

    # validating food object
    if order_obj.validate_food_obj(new_food):
        food_name = new_food["food_name"]
        food_price = new_food["food_price"]

        # validating empty input and input data type
        invalid_input = order_obj.validate_input(new_food, ["food_name", "food_price" ], ["food_price"], ["food_name"])
        if invalid_input:
            return jsonify(invalid_input), 400

        # check whether food item exists
        if order_obj.check_existing_food(food_name) :
            return jsonify({"error": "food item duplication"}), 400

         #Adding the food item to te menu
        new_saved_food = order_obj.add_food(food_name, food_price)
        return jsonify(new_saved_food), 201

    message2 = {"error": "invalid food object. must be { 'food_name':  'food_price': ' } "}
    return jsonify(message2), 400


#a function to fetch all foods list by admin
@My_blue.route('/api/v1/menu', methods=['GET'])
@token_required
@swag_from('../docs/get_menu.yml')
def get_all_foods_list(current_user):
    "A function to fetch all menu food items"
    return jsonify(order_obj.get_all_foods()), 200



@My_blue.route('/api/v1/users/orders', methods = ["GET"])
@token_required
@swag_from('../docs/order_history.yml')
def get_user_order_history(current_user):

    return  jsonify(querry.get_user_Order_history(current_user)), 200


#A function to act as index page , to offer description to the user
@My_blue.route('/menu', methods=['GET'])
@swag_from('../docs/index.yml')
def index():
    "A function to act as the index page for the API"
    return   jsonify( {"Get all orders" : "GET, api/v1/orders",
                       "Register User": "POST, api/v1/auth/signup",
                       "Login user": "POST , api/v1/auth/login",
                       "Get user order History": "GET, api/v1/users/order",
                      "Place anew order " :"POST ,  api/v1/users/orders",
                      "Fetch a specific order" : "GET , api/v1/orders/oder-uuid",
                      "Update an order status" : "PUT, api/v1/orders/order-uuid",
                      "Fetch all food items on the menu" : "GET, api/v1/menu",
                      "Add food item to menu" : "POST, api/v1/menu ",
                      "Index page" : " GET  ,/"} ), 200
