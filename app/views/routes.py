from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import json
from app.models.orders import Orders


My_app = Flask(__name__, instance_relative_config=True)

order_obj = Orders()


# A function to fetch all orders
@My_app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    if order_obj.get_all_orders():
        return jsonify(order_obj.get_all_orders()) , 200
    else :
        return jsonify ({"Message" :"Empty order list" }), 404

#A function to place_order
@My_app.route('/api/v1/orders', methods=['POST'])
def place_order():
    if request.data:
        new_oder = request.json
        if order_obj.validate_order_obj(new_oder):
            order_food_id = new_oder["order_food_id"]
            order_quantity = new_oder["order_quantity"]
            order_client = new_oder["order_client"]

            if order_obj.orders_list:
                if order_obj.check_existing_order(order_food_id,order_client ):
                    message1 = {"ERROR": "same oder_food has been paced today , please oder for a different food item"}
                    return jsonify(message1), 406
                else :

                    if order_obj.food_list:
                        if order_obj.check_existing_food_id(order_food_id):
                            order_obj.place_order(order_food_id, order_quantity,order_client)
                            return jsonify({"Order created succesfully" :order_obj.orders_list},
                                           {"Available food list" : order_obj.food_list}),201

                        else:
                            message2 ={"Error" : "Food_id requested doesnt exist ",
                                      "Available food list" : order_obj.food_list
                                      }
                            return jsonify(message2),404
                    else:
                        return jsonify({ "Empty food list" : "contact Admin to add food items"}),404

            else:
                if order_obj.food_list:
                    if order_obj.check_existing_food_id(order_food_id):
                        order_obj.place_order(order_food_id, order_quantity, order_client)
                        return jsonify({"Order created succesfulyy":order_obj.orders_list},
                                       {"Available food list": order_obj.food_list}), 201

                    else:
                        message3 = {"Error": "Food_id requested doesnt exist ",
                                    "Available food list": order_obj.food_list
                                    }
                        return jsonify(message3),404
                else:
                    return jsonify({"Empty food list": "contact Admin to add food items"}),404



        else:
            message2 = {"ERROR" : "invalid order object",
                "Help" : "order object should be in {'order_food_id' : id ,'order_quantity': qty, 'order_client':name}"
             }
            return jsonify(message2),406

    else:
        return jsonify({"ERROR" : "Empty order posted"}) ,406









