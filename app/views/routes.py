"A module for setting up the API  strings"

from flask import Flask
from flask import jsonify
from flask import request
from app.models.orders import Orders


My_app = Flask(__name__)

order_obj = Orders()


# A function to fetch all orders
@My_app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    "A function to fetch all orders"
    if order_obj.get_all_orders():
        return jsonify(order_obj.get_all_orders()), 202
    return jsonify({"Message": "Empty order list"}), 200


#A function to place_order
@My_app.route('/api/v1/orders', methods=['POST'])
def place_order():
    " a function to place an order"
    #checking empty request data
    if request.data:
        new_oder = request.json

        #validating the order object
        if order_obj.validate_order_obj(new_oder):
            order_food_id = new_oder["order_food_id"]
            order_quantity = new_oder["order_quantity"]
            order_client = new_oder["order_client"]

              #checking for existing oder
            if order_obj.check_existing_order(order_food_id, order_client) or  order_food_id =="" \
                    or  order_quantity == ""  or  order_client == "":
                message1 = {"Error": "Order already exist or Missing order Fields,"
                                     " please order for a different food item"}
                return jsonify(message1), 406
            else:
                if order_obj.check_existing_food(order_food_id):
                    order_obj.place_order(order_food_id, order_quantity, order_client)
                    return jsonify({"Order created succesfully": order_obj.orders_list},
                                   {"Available food list": order_obj.food_list}), 201

                message2 = {"Error": "Unable to find food id  ",
                            " See available food list": order_obj.food_list}

                return jsonify(message2), 200


        message2 = {"ERROR": "invalid order object",
                    "Help": "order object should be  "
                            "{'order_food_id' : id ,'order_quantity': qty, "
                            "'order_client':name}"}
        return jsonify(message2), 406

    return jsonify({"ERROR": "Empty order posted"}), 406

#A function for admin to add food items to the menu
@My_app.route('/api/v1/menu/add', methods=['POST'])
def add_food_iems():
    "A function that adds food items"
    #checking empty response content
    if request.data:
        new_food = request.json

        #validating food object
        if order_obj.validate_food_obj(new_food):
            food_name = new_food["food_name"]
            food_price = new_food["food_price"]

            # check whether food item exists
            if order_obj.check_existing_food(food_name) or  food_name ==""  or food_price == "":
                return jsonify({"ERROR": "Food item already exists or Empty order fields"}), 406
            order_obj.add_food(food_name, food_price)
            return jsonify("SUCCESFULY ADDED FOOD TO MENU", order_obj.get_all_foods()), 201
        message2 = {"Validation Error": "invalid food object ",
                    "Help": "food object should be {'food_name' : name ,'food_price': price}"}
        return jsonify(message2), 406
    return jsonify({"ERROR": "Empty  content"}), 200


#a function to fetch all foods list by admin
@My_app.route('/api/v1/menu', methods=['GET'])
def get_all_foodslist():
    "A function to fetch all menu food items"

    #checking whethr menu list is empty
    if order_obj.food_list:
        return jsonify(order_obj.get_all_foods()), 202
    return jsonify({"Empty menu": "Please add foods list "}), 200


#A function to fetch a specific order by uuid
@My_app.route('/api/v1/orders/<order_uuid>', methods=['GET'])
def fetch_order(order_uuid):
    "A function to fetch a specified order by uuid"
    the_order = {}
    #checking if the order list contains data
    if order_obj.orders_list:
        the_order = order_obj.fetch_order_by_uuid(order_uuid)
        if the_order:
            return jsonify(the_order), 202
        return jsonify({"ERROR": "Unable to find order"}), 406
    return jsonify({"MESSAGE": "Empty order List"}), 200


#A function that updates order status
@My_app.route('/api/v1/orders/<order_uuid>', methods=['PUT'])
def update_order_status(order_uuid):
    "A function to update the status of an order by uuid"

    if request.data:
        new_status_obj = request.json
        #validating status object and status
        if "order_status" in new_status_obj :

            new_status = new_status_obj["order_status"]
            updated_order = order_obj.update_order_status(order_uuid, new_status)
            if updated_order :
               return jsonify( updated_order), 202

            else:
                  message =({"Error": "Unable to find order"})
        else:
            message = {"Invalid status object": "status should be {'order_status': status} "
                         "and  status must be in [ok, yes, no]"}
        return jsonify(message) ,406
    else:
        return jsonify({"ERROR": "Empty content"}), 406


#A function to act as index page , to offer description to the user
@My_app.route('/', methods=['GET'])
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
