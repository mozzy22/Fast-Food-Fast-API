from flask import  Blueprint, jsonify, request
My_blue = Blueprint('menu', __name__ )
from app.models.orders import Orders
#from routes import order_obj
order_obj = Orders()

#A function for admin to add food items to the menu
@My_blue.route('/api/v1/menu/add', methods=['POST'])
def add_food_iems():
    "A function that adds food items"
    #checking empty response content
    try:
        new_food = request.json
    except Exception:
        return jsonify({"ERROR": "Empty  content"}), 200

    # validating food object
    if order_obj.validate_food_obj(new_food):
        food_name = new_food["food_name"]
        food_price = new_food["food_price"]

        # check whether food item exists
        if order_obj.check_existing_food(food_name) or not food_name or not food_price:
            return jsonify({"ERROR": "Food item already exists or Empty order fields"}), 406

         #Adding the food item to te menu
        order_obj.add_food(food_name, food_price)
        return jsonify("SUCCESFULY ADDED FOOD TO MENU", order_obj.get_all_foods()), 201

    message2 = {"Validation Error": "invalid food object ",
                "Help": "food object should be {'food_name' : name ,'food_price': price}"}
    return jsonify(message2), 406


#a function to fetch all foods list by admin
@My_blue.route('/api/v1/menu', methods=['GET'])
def get_all_foodslist():
    "A function to fetch all menu food items"

    #checking whethr menu list is empty
    if order_obj.food_list:
        return jsonify(order_obj.get_all_foods()), 202
    return jsonify({"Empty menu": "Please add foods list "}), 200



#A function to act as index page , to offer description to the user
@My_blue.route('/', methods=['GET'])
def index():
    "A function to act as the index page for the API"
    return   jsonify(" WELCOME TO THE FAST-FOOD-FAST  API",
                     "Fast-Food-Fast is a food delivery service app for a restaurant",
                     "See the  Features and their endpoints",
                     {"Get all orders" : "GET, api/v1/orders",
                      "Place anew order " :"POST ,  api/v1/orders",
                      "Fetch a specific order" : "GET , api/v1/orders/oder-uuid",
                      "Update an order status" : "PUT, api/v1/orders/order-uuid",
                      "Fetch all food items on the menu" : "GET, api/v1/menu",
                      "Add food item to menu" : "POST, api/v1/menu/add ",
                      "Index page" : " GET  ,/"},
                     "WISH YOU ALL THE BEST AS YOU DINE WITH US"), 202
