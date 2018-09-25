"A module for setting up the API routes"

from flask import Flask, jsonify, request
from app.views.menu_blueprint import My_blue,order_obj


My_app = Flask(__name__)
My_app.register_blueprint(My_blue)

#order_obj = Orders()


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

    try :
        new_oder = request.json
    except Exception:
        return jsonify({"ERROR": "Empty content posted"}), 406

    # validating the order object
    if order_obj.validate_order_obj(new_oder):
        order_food_id = new_oder["order_food_id"]
        order_quantity = new_oder["order_quantity"]
        order_client = new_oder["order_client"]

        # checking whether the order already exists
        if order_obj.check_existing_order(order_food_id, order_client) or not order_food_id \
                or not order_quantity or not order_client:
            message1 = {"Error": "Order already exist or Missing order Fields,"
                                 " please order for a different food item"}
            return jsonify(message1), 406
        else:
            #checking whether the food item requested for exists
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


#A function to fetch a specific order by uuid
@My_app.route('/api/v1/orders/<order_uuid>', methods=['GET'])
def fetch_order(order_uuid):
    "A function to fetch a specified order by uuid"

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

    try :
        new_status_obj = request.json
    except Exception:
        return jsonify({"ERROR": "Empty content"}), 406

        #validating status object and status
    if "order_status" in new_status_obj:

        new_status = new_status_obj["order_status"]
        updated_order = order_obj.update_order_status(order_uuid, new_status)
        if updated_order:
            return jsonify(updated_order), 202

        message = ({"Error": "Unable to find order"})
    else:
        message = {"Invalid status object": "status should be {'order_status': status} "
                                            "and  status must be in [ok, yes, no]"}
    return jsonify(message), 406


