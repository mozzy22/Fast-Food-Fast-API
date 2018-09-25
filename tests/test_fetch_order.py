"A module dor testing the fetch order feature"
import unittest
from app.models.orders import Orders
from app.views.routes import My_app
from app.views.menu_blueprint import order_obj
from config.config import app_config

class TestCase(unittest.TestCase):
    "A test classs for fetch order feature"


    def setUp(self):
        " setting up variables to run before test"
        self.order_obj = Orders()
        self.hostname = "http://localhost:5000/api/v1/"
        self.order = {
            "order_id" : 1,
            "order_uuid" : "rigt_uuid",
            "order_food_id" : 1,
            "order_quantity" : "1",
            "order_created_at" : "13/04/2016",
            "order_status" : "pendng",
            "order_client" :"mutesasira"
        }
        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()

    def test_empty_list(self):
        "A mehtod to test empty model orders list"
        self.assertEqual(len(self.order_obj.get_all_orders()), 0)

    def test_fetch_order_method(self):
        "testing model fetch order method  returns an order with valid uuid"
        self.order_obj.orders_list.append(self.order)
        self.assertEqual(self.order_obj.fetch_order_by_uuid("rigt_uuid"), self.order)

    def test_fetch_order_method_wrong_uuid(self):
        "testing model fetch order method doesnt return an order with invalid uuid"
        self.order_obj.orders_list.append(self.order)
        self.assertEqual(self.order_obj.fetch_order_by_uuid("wrong_uuid"), {})

    def test_fetch_order_method_wrong_uuid2(self):
        "testing model fetch order method doesnt return an order with invalid uuid"
        self.order_obj.orders_list.append(self.order)
        self.assertEqual(len(self.order_obj.fetch_order_by_uuid("wrong_uuid")), 0)

    def test_right_get_method(self):
        "asserting a correct method returns an empty response if order list is empty"
        resp = self.app.get(self.hostname + "orders/string-uuid")
        self.assertEqual(resp.status_code, 200)

    def test_status_code_for_right_uuid(self):
        "asserting a request with invalid uuid is  returned"
        order_obj.orders_list.append(self.order)
        resp = self.app.get(self.hostname + "orders/rigt_uuid")
        self.assertEqual(resp.status_code, 202)

    def test_status_code_for_invalid_uuid(self):
        "asserting a request with invalid uuid is not returned"
        order_obj.orders_list.append(self.order)
        resp = self.app.get(self.hostname + "orders/wrong_uuid")
        self.assertEqual(resp.status_code, 406)

    def tearDown(self):
        "A method to reset data structures"
        order_obj.orders_list.clear()
        self.order_obj.orders_list.clear()



if __name__ == "__main__":
    unittest.main()
