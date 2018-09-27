"A module to test the status update feature"
import unittest
import json
from app.views.routes import My_app, order_obj
from app.views.menu_blueprint import order_obj
from config.config import app_config
from app.models.orders import Orders

class TestCase(unittest.TestCase):
    "A class for testing the update status feature"


    def setUp(self):
        " setting up variables to run before test"
        self.hostname = "http://localhost:5000/api/v1/"
        self.order_obj = Orders()
        # valid status objet to be posted
        self.status = {
            "order_status" : "ok"
        }

      #invalid status to be pasted
        self.invalid_status = {
            "order_status": "null"
        }
      #invalid status format
        self.invalid_status_obj = {
            "orderstatus": "yes"
        }

        self.order = {
            "order_id": 1,
            "order_uuid": "rigt_uuid",
            "order_food_id": 1,
            "order_quantity": "1",
            "order_created_at": "13/04/2016",
            "order_status": "pendng",
            "order_client": "mutesasira"
        }

        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()

    #Testing the model method
    def test_empty_order_list(self):
        "asserting orders list is empty"
        self.assertEqual(len(self.order_obj.orders_list), 0)

    def test_update_valid_uuid(self):
        "asserting that the method is updated"
        self.order_obj.orders_list.append(self.order)
        updated_order = self.order_obj.update_order_status("rigt_uuid", "ok")
        self.assertEqual(updated_order['order_status'], "Completed")

    def test_update_valid_uuid1(self):
        "asserting that the method is updated"
        self.order_obj.orders_list.append(self.order)
        updated_order = self.order_obj.update_order_status("rigt_uuid", "yes")
        self.assertEqual(updated_order['order_status'], "Accepted")

    def test_update_valid_uuid2(self):
        "asserting that the method is updated"
        self.order_obj.orders_list.append(self.order)
        updated_order = self.order_obj.update_order_status("rigt_uuid", "no")
        self.assertEqual(updated_order['order_status'], "Rejected")

    def test_update_invalid_uuid(self):
        "asserting that the method is not updated with a wrong status"
        self.order_obj.orders_list.append(self.order)
        updated_order = self.order_obj.update_order_status("wrong_uuid", "no")
        self.assertEqual(updated_order, {})

     #Testing the routes

    def test_put_valid_uuid_empty_orderlist(self):
        "checking status code when order list is empty"
        resp = self.app.put(self.hostname + "orders/rigt_uuid", data=json.dumps(self.status),
                            content_type='application/json')
        self.assertEqual(resp.status_code, 406)


    def test_put_valid_uuid_with_orderlist(self):
        "checking status code when right order uuid is posted , with order list"
        order_obj.orders_list.append(self.order)
        resp = self.app.put(self.hostname + "orders/rigt_uuid", data=json.dumps(self.status),
                            content_type='application/json')
        self.assertEqual(resp.status_code, 200)


    def test_put_invalid_status_with_orderlist(self):
        "checking status code when invalid status object is posted"
        order_obj.orders_list.append(self.order)
        resp = self.app.put(self.hostname + "orders/rigt_uuid",
                            data=json.dumps(self.invalid_status_obj), content_type='application/json')

        self.assertEqual(resp.status_code, 406)


    def tearDown(self):
        self.order_obj.orders_list.clear()
        order_obj.orders_list.clear()


if __name__ == "__main__":
    unittest.main()
