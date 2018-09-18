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
        return jsonify ({"Error" : "empty result list"}), 404




