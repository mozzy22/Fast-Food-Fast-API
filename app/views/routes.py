"A module for setting up the API  strings"

from flask import Flask
from flask import jsonify
from flask import request
from app.models.orders import Orders


My_app = Flask(__name__, instance_relative_config=True)

order_obj = Orders()


# A function to fetch all orders
@My_app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    "A function to fetch all orders"
    if order_obj.get_all_orders():
        return jsonify(order_obj.get_all_orders()), 202
    else:
        return jsonify({"Message" :"Empty order list"}), 200

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

           #checking for empty order lists
            if order_obj.orders_list:
                #checking  whether order exists
                if order_obj.check_existing_order(order_food_id, order_client):
                    message1 = {"ERROR": "same oder_food has been paced today ,"
                                         " please oder for a different food item"}
                    return jsonify(message1), 406
                else:
                    #checking for foof list in menu
                    if order_obj.food_list:
                        #checking whethr posted food id exists in the menu
                        if order_obj.check_existing_food_by_id(order_food_id):
                            order_obj.place_order(order_food_id, order_quantity, order_client)
                            return jsonify({"Order created succesfully" :order_obj.orders_list},
                                           {"Available food list" : order_obj.food_list}), 201

                        else:
                            message2 = {"Error" : "Food_id requested doesnt exist ",
                                        "Available food list" : order_obj.food_list
                                      }
                            return jsonify(message2), 200
                    else:
                        return jsonify({"Empty food list" : "contact Admin to add food items"}), 200

            else:
                #checking empty food list
                if order_obj.food_list:
                    # checking whethr posted food id exists in the menu
                    if order_obj.check_existing_food_by_id(order_food_id):
                        order_obj.place_order(order_food_id, order_quantity, order_client)
                        return jsonify({"Order created succesfuly":order_obj.orders_list},
                                       {"Available food list": order_obj.food_list}), 201

                    else:
                        message3 = {"Error": "Food_id requested doesnt exist ",
                                    "Available food list": order_obj.food_list
                                    }
                        return jsonify(message3), 200
                else:
                    return jsonify({"Empty food list": "contact Admin to add food items"}), 200



        else:
            message2 = {"ERROR" : "invalid order object",
                        "Help" : "order object should be  "
                                 "{'order_food_id' : id ,'order_quantity': qty, 'order_client':name}"}

            return jsonify(message2), 406

    else:
        return jsonify({"ERROR" : "Empty order posted"}), 406


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

            if order_obj.food_list:
                # check whether food item exists
                if order_obj.check_existing_food_by_name(food_name):
                    return jsonify({"ERROR": "Food item already exists"}), 406
                else:
                    order_obj.add_food(food_name, food_price)
                    return jsonify("SUCCESFULY ADDED FOOD TO MENU", order_obj.get_all_foods()), 201

            else:
                    order_obj.add_food(food_name, food_price)
                    return jsonify("SUCCESFULY ADDED FOOD TO MENU", order_obj.get_all_foods()), 201

        else:
            message2 = {"ERROR": "invalid food object",
                            "Help": "food object should be {'food_name' : name ,'food_price': price}"}
            return jsonify(message2), 406


    else:
        return jsonify({"ERROR": "Empty food content"}), 200

#a function to fetch all foods list by admin
@My_app.route('/api/v1/menu', methods=['GET'])
def get_all_foodslist() :
     "A function to fetch all menu food items"

     #checking whethr menu list is empty
     if order_obj.food_list:
         return jsonify(order_obj.get_all_foods()), 202
     else:
         return jsonify({"Empty menu" : "Please add foods list "}), 200


#A function to fetch a specific order by uuid
@My_app.route('/api/v1/orders/<order_uuid>', methods=['GET'])
def fetch_order(order_uuid):
    the_order = {}
    #checking if the order list contains data
    if order_obj.orders_list:
       the_order = order_obj.fetch_order_by_uuid(order_uuid)
       if the_order:
            return jsonify(the_order), 202
       else:
            return jsonify({"ERROR": "The order requested for doent exist"}), 406
    else:
        return jsonify({"MESSAGE": "No order placed yet"}), 200

#A function that updates order status
@My_app.route('/api/v1/orders/<order_uuid>', methods=['PUT'])
def update_order_status(order_uuid):
    updated_order = {}
    if request.data:
        new_status_obj = request.json
        if ("order_status" in new_status_obj):
            new_status = new_status_obj["order_status"]
            if new_status in ["ok", "yes" , "no"]:
                 updated_order = order_obj.update_order_status(order_uuid,new_status)
                 if updated_order :
                     return jsonify("SUCCESFULLY UPDATED ORDER STATUS",updated_order)
                 else:
                     return jsonify({"Message" : "Oder UUID requested doesnt exist"})

            else:
                return jsonify({"ERROR" : "Unknown status. staus must be in [ok, yes, no]"})
        else:
            return jsonify({"Invalid status object" : "status should be {'order_status': status}"})
    else:
        return jsonify({"ERROR": "Empty status update content"}), 200









