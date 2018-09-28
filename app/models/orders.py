"A module for the orders model"

import uuid
import datetime
__author__ = "Mutesasira Moses"

class Orders:
    "a model class for the orders made by clients"

# declaring status constants
    STATUS1 = "Pending"
    STATUS2 = "Accepted"
    STATUS3 = "Rejected"
    STATUS4 = "Completed"

    def __init__(self):
        "innitialising all class members of the order - model"
        self.orders_list = []
        self.order = {}
        self.order_id = 0
        self.order_uuid = ""
        self.order_food_id = ""
        self.order_quantity = ""
        self.order_created_at = ""
        self.order_status = ""
        self.order_client = ""

        #innitalising class members forthe food
        self.food_id = 0
        self.food_name = ""
        self.food_price = ""
        self.food = {}
        self.food_list = []


    def get_all_orders(self):
        "a method that gets all orders"
        return self.orders_list


    def place_order(self, order_food_id, order_quantity, order_client):
        "A method to place a new order"
        self.order_id = len(self.orders_list) + 1
        self.order_uuid = str(uuid.uuid1())
        self.order_food_id = order_food_id
        self.order_quantity = order_quantity
        self.order_created_at = datetime.datetime.now().strftime('%Y-%m-%d-%H')
        self.order_status = Orders.STATUS1
        self.order_client = order_client

        self.order = {
            "order_id" : self.order_id,
            "order_uuid" : self.order_uuid,
            "order_food_id" : self.order_food_id,
            "order_quantity" : self.order_quantity,
            "order_created_at" : self.order_created_at,
            "order_status"  : self.order_status,
            "order_client" : self.order_client
        }
        self.orders_list.append(self.order)
        return self.order

    def validate_order_obj(self, order_Obj):
        "A method to validate a user object"
        if ("order_food_id" in order_Obj and "order_quantity" in order_Obj and
                    "order_client" in order_Obj):
            return True
        return False

    def get_all_foods(self):
        "A method to return all availabe food list"
        return self.food_list


    def add_food(self, food_name, food_price):
        "A  method to add foods items to the menu"
        self.food_id = len(self.food_list) + 1
        self.food_name = food_name
        self.food_price = str(food_price) + "$"
        self.food = {
            "food_id": self.food_id,
            "food_name": self.food_name,
            "food_price": self.food_price}
        self.food_list.append(self.food)
        return self.food


    def validate_food_obj(self, food_Obj):
        "A method to validate a food object"
        if ("food_name" in food_Obj and "food_price" in food_Obj):
            return True
        return False


    def check_existing_order(self, order_food_id, order_client):
        "a method to check whethr a given order already exists"
        exist = False
        order_created_at = datetime.datetime.now().strftime('%Y-%m-%d-%H')

        for order in self.orders_list:
            if order["order_food_id"] == order_food_id and order["order_client"] == order_client \
                    and order["order_created_at"] == order_created_at:
                exist = True
                break
            else:
                exist = False
        return exist


    def check_existing_food(self, value):
        "A method to check whether a given food item already exists on the menu"
        key = ""
        if isinstance(value, int):
            key = "food_id"
        elif isinstance(value, str):
            key =  "food_name"
        exist = False
        for food in self.food_list:
            if food[key] == value:
                exist = True
                break
            else:
                exist = False
                # print(food)
        return exist


    def fetch_order_by_uuid(self, order_uuid):
        "A method to fetch a specific order"
        my_order = {}
        for order in self.orders_list:
            if order["order_uuid"] == order_uuid:
                my_order = order
                break
            else:
                pass
        return my_order

    def update_order_status(self, order_uuid, status):
        my_order = self.fetch_order_by_uuid(order_uuid)
        if my_order:
            if status == "yes":
                my_order["order_status"] = Orders.STATUS2
            elif status == "no":
                my_order["order_status"] = Orders.STATUS3
            elif status == "ok":
                my_order["order_status"] = Orders.STATUS4
            else:
                my_order["order_status"] = Orders.STATUS1
        else:
            pass
        return my_order

    def validate_input(self,input, validation_data,validation_int_type, validation_str_type ):
        "method to validate input"
        error_message = []
        #validating empty input
        for data in validation_data:
            try:
                input[data]
                # Check for empty input
                if not input[data]:
                    raise Exception
            except:
                error_message.append({"error" :data + ' is required'})
        #validating int data type
        for data in validation_int_type :
            self.check_datatype(data, int,input, error_message)

         #validating str datatype
        for data in validation_str_type:
            self.check_datatype(data, str,input, error_message)
        # return errors
        return error_message

    #method to check data type
    def check_datatype(self,data, data_type ,input,  error_message):
        try:
            # Check for empty input
            if not isinstance(input[data], data_type):
                raise Exception

        except:
            error_message.append({"error": " invalid " + str(data) + " data_type .<" + data_type.__name__ +"> recquired"})


