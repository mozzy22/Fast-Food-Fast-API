import uuid
__author__ = "Mutesasira Moses"

class Orders:
    "a model class for the orders made by clients"

    def __init__(self):
        "innitialising all class members of the order - model"
        self.orders_list = []
        self.order  = {}
        self.order_id = 0
        self.order_uuid = ""
        self.order_food = ""
        self.order_quantity = ""
        self.order_price = ""
        self.order_created_at = ""
        self.order_status = ""
        self.order_client = ""



    def get_all_orders(self):
        "a function that gets all orders"
        return self.orders_list



