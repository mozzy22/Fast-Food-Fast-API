"A module for setting up the API routes"

from flask import Flask, jsonify, request
from app.views.menu_blueprint import My_blue,order_obj
from app.views.user_blueprint import user_blue


My_app = Flask(__name__)
My_app.register_blueprint(My_blue)
My_app.register_blueprint(user_blue)


# A function to fetch all orders
@My_app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    "A function to fetch all orders"
    return jsonify(order_obj.get_all_orders()), 200


#A function to place_order
@My_app.route('/api/v1/orders', methods=['POST'])
def place_order():
    " a function to place an order"
    new_oder = request.json

    # validating the order object
    if order_obj.validate_order_obj(new_oder):
        order_food_id = new_oder["order_food_id"]
        order_quantity = new_oder["order_quantity"]
        order_client = new_oder["order_client"]

         #validating empty input and input data type
        invalid_input = order_obj.validate_input(new_oder, ["order_food_id", "order_quantity", "order_client" ]
                                               ,["order_quantity","order_food_id", "order_client"], [ ])
        if invalid_input:
            return jsonify(invalid_input), 400

        # checking whether the order already exists
        if order_obj.check_existing_order(order_food_id, order_client) :
            message1 = {"error": "order duplication"}
            return jsonify(message1), 400
        else:
            #checking whether the food item requested for exists
            if order_obj.check_existing_food(order_food_id):
                saved_order = order_obj.place_order(order_food_id, order_quantity, order_client)
                return jsonify(saved_order), 201


            message2 = {"error": "unable to find food id  "}

            return jsonify(message2), 404

    message2 = {"error": "invalid order object. must be { 'order_food_id': 'order_quantity': 'order_client': }" }
    return jsonify(message2), 400


#A function to fetch a specific order by uuid
@My_app.route('/api/v1/orders/<order_uuid>', methods=['GET'])
def fetch_order(order_uuid):
    "A function to fetch a specified order by uuid"

    the_order = order_obj.fetch_order_by_uuid(order_uuid)
    if the_order:
        return jsonify(the_order), 200
    return jsonify({"error": "unable to find order"}), 404


#A function that updates order status
@My_app.route('/api/v1/orders/<order_uuid>', methods=['PUT'])
def update_order_status(order_uuid):
    "A function to update the status of an order by uuid"

    new_status_obj = request.json

        #validating status object and status
    if "order_status" in new_status_obj:

        new_status = new_status_obj["order_status"]

        #validating empty input and input data types
        invalid_input = order_obj.validate_input(new_status_obj, ["order_status"],[],["order_status"])
        if invalid_input:
            return jsonify(invalid_input), 400
        updated_order = order_obj.update_order_status(order_uuid, new_status)
        if updated_order:
            return jsonify(updated_order), 200

        message = ({"error": "unable to find order"})
    else:
        message = {"error": "invalid status object . must be {'order_status':  }"}
    return jsonify(message), 400

#error handlers
@My_app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "bad reqeust"}), 400

@My_app.errorhandler(401)
def not_authorized(e):
    return jsonify({"error": "not authorized."}), 401


@My_app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "url does not exist"}), 404


@My_app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "method not allowed"}), 405

