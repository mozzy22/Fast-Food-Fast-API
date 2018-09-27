"A module to test get all orders feature"
import unittest
from app.models.orders import Orders
from app.views.routes import My_app
from app.views.menu_blueprint import order_obj
from config.config import app_config

class TestCase(unittest.TestCase):
    "A class for testing the get all orders feature"

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
        "A method to test model object creation"
        self.assertIsInstance(self.order_obj1, Orders)

    def test_empty_list(self):
        "Asserting no dummy data in model object"
        self.assertEqual(len(self.order_obj1.get_all_orders()), 0)

    def test_add_list(self):
        "Asserting that list can be added to"
        self.order_obj1.orders_list.append(self.order)
        self.assertEqual(len(self.order_obj1.get_all_orders()), 1)

    def test_right_get_method(self):
        "asserting a correct method returns an empty response"
        resp = self.app.get(self.hostname + "orders")
        self.assertEqual(resp.status_code, 200)


    def test_right_get_method2(self):
        "asserting a correct method returns an  response with data"
        order_obj.orders_list.append(self.order)
        resp = self.app.get(self.hostname + "orders")
        self.assertEqual(resp.status_code, 200)

    def test_return_data(self):
        "Asserting that right data is returned on a get request"
        order_obj.orders_list.append(self.order)
        resp = self.app.get(self.hostname + "orders")
        self.assertIn('mutesasira', str(resp.data))

    def test_index(self):
        "Testingthat a right status code is returned on calling the get request of index url"
        resp = self.app.get()
        self.assertEqual(resp.status_code, 200)


    def tearDown(self):
        "Reseting parameters after tests"
        order_obj.orders_list.clear()



if __name__ == "__main__":
    unittest.main()
