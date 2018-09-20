import unittest
from app.models.orders import Orders
from app.views.routes import My_app
from app.views.routes import order_obj
from config.config import app_config

class Test_Case(unittest.TestCase):


    def setUp(self):
        " setting up variables to run before test"
        self.order_obj1 = Orders()
        self.hostname = "http://localhost:5000/api/v1/"
        self.order = {
            "order_id" : 1,
            "order_uuid" : "essssss",
             "order_food_id" : 1,
            "order_quantity" : "1",
            "order_created_at" : "13/04/2016",
            "order_status" : "pendng",
            "order_client" :"mutesasira"
        }
        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()


    def test_model_creation(self):
        self.assertIsInstance(self.order_obj1, Orders)

    def test_empty_list(self):
        self.assertEqual(len(self.order_obj1.get_all_orders()),0)

    def test_add_list(self):
        self.order_obj1.orders_list.append(self.order)
        self.assertEqual(len(self.order_obj1.get_all_orders()), 1)

    def test_right_get_method(self):
        "asserting a correct method returns an empty response"
        resp = self.app.get(self.hostname + "orders")
        self.assertEqual(resp.status_code, 200)

    def test_return_message(self):
        resp = self.app.get(self.hostname + "orders")
        self.assertIn("Message\": \"Empty order list", str(resp.data))

    def test_right_get_method(self):
        "asserting a correct method returns an  response with data"
        order_obj.orders_list.append(self.order)
        resp = self.app.get(self.hostname + "orders")
        self.assertEqual(resp.status_code, 202)

    def test_return_data(self):
        order_obj.orders_list.append(self.order)
        resp = self.app.get(self.hostname + "orders")
        self.assertIn('mutesasira', str(resp.data))

    def tearDown(self):
         order_obj.orders_list.clear()



if __name__ == "__main__":
    unittest.main()
