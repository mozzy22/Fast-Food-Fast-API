from flask import  Blueprint, jsonify, request
from app.models.orders import Orders

My_blue = Blueprint('menu', __name__ )
#from routes import order_obj
order_obj = Orders()

#A function for admin to add food items to the menu
@My_blue.route('/api/v1/menu/add', methods=['POST'])
def add_food_items():
    "A function that adds food items"
    #checking empty response content

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
            return jsonify({"error": "food item duplication"}), 406

         #Adding the food item to te menu
        order_obj.add_food(food_name, food_price)
        return jsonify(order_obj.food_list), 201

    message2 = {"error": "invalid food object "}
    return jsonify(message2), 400


#a function to fetch all foods list by admin
@My_blue.route('/api/v1/menu', methods=['GET'])
def get_all_foodslist():
    "A function to fetch all menu food items"
    return jsonify(order_obj.get_all_foods()), 200


#A function to act as index page , to offer description to the user
@My_blue.route('/', methods=['GET'])
def index():
    "A function to act as the index page for the API"
    return   jsonify( {"Get all orders" : "GET, api/v1/orders",
                      "Place anew order " :"POST ,  api/v1/orders",
                      "Fetch a specific order" : "GET , api/v1/orders/oder-uuid",
                      "Update an order status" : "PUT, api/v1/orders/order-uuid",
                      "Fetch all food items on the menu" : "GET, api/v1/menu",
                      "Add food item to menu" : "POST, api/v1/menu/add ",
                      "Index page" : " GET  ,/"} ), 200
