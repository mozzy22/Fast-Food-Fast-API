import unittest
import json
from app.models.orders import Orders
from app.views.routes import My_app
from app.views.routes import order_obj
from config.config import app_config

class Test_Case(unittest.TestCase):


    def setUp(self):
        " setting up variables to run before test"
        self.order_obj = Orders()
        self.hostname = "http://localhost:5000/api/v1/"
        self.complete_order ={
            "order_id": 1,
            "order_uuid": 69696969,
            "order_food_id": 3,
            "order_quantity": 3,
            "order_created_at": "12/03/2016" ,
            "order_status": "pending",
            "order_client": "mutesasira"

        }
        self.order = {
             "order_food_id" : 1,
            "order_quantity" : "1",
            "order_client" :"mutesasira"
        }

        self.order_invalid_food_id = {
            "order_food_id": 9,
            "order_quantity": "1",
            "order_client": "mutesasira"
        }

        self.invalid_order = {
            "order_quantity": "1",
            "order_client": "mutesasira"
        }



        self.food = {
            "food_name": "fish",
            "food_price": "25$"
        }

        self.food_invalid = {
            "inavlid key": "fish",
            "food_price": "25$"
        }
        order_obj.add_food("pizza", "20$")

        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()

#testing the model methods
    def test_model_creation(self):
        self.assertIsInstance(self.order_obj, Orders)

    def test_empty_model_oder_list(self):
        self.assertEquals(len(self.order_obj.get_all_orders()), 0)

    def test_place_order(self):
        self.order_obj.place_order(1,3,"moses")
        self.assertEquals(len(self.order_obj.get_all_orders()), 1)

    def test_validate_order(self):
         self.assertFalse(self.order_obj.validate_order_obj(self.invalid_order))

    def test_empty_food_list(self):
        self.assertEqual(len(self.order_obj.get_all_foods()),0)

    def test_add_food(self):
         self.order_obj.add_food("pizza", "20$")
         self.assertEqual(len(self.order_obj.get_all_foods()),1)

    def test_validate_food(self):
         self.assertTrue(self.order_obj.validate_food_obj(self.food))

    def test_validate_food2(self):
        self.assertFalse(self.order_obj.validate_food_obj(self.food_invalid))


    def test_check_exist_order(self):
         self.order_obj.place_order(1, 3, "moses")
         self.assertTrue(self.order_obj.check_existing_order(1,"moses"))

    def test_check_exist_order2(self):
        self.order_obj.place_order(1, 3, "moses")
        self.assertFalse(self.order_obj.check_existing_order(2, "moses"))

    def test_exist_food_id(self):
        self.order_obj.add_food("pizza", "20$")
        self.assertTrue(self.order_obj.check_existing_food_id(1))

    def test_exist_food_id2(self):
        self.order_obj.add_food("pizza", "20$")
        self.order_obj.add_food("chicken", "20$")
        self.assertFalse(self.order_obj.check_existing_food_id(3))


#Testing the routes
    def test_empty_list(self):
        self.assertEqual(len(order_obj.get_all_orders()),0)

    def test_post_valid_order(self):
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 1)
        print(str(resp.data))

    def test_post_valid_order2(self):
        order_obj.orders_list.append(self.complete_order)
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 2)

    def test_post_invalid_order2(self):
        order_obj.orders_list.append(self.complete_order)
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.invalid_order), content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 1)

    def test_post_invalid_order3(self):
        order_obj.orders_list.append(self.complete_order)
        order_obj.food_list.clear()
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 1)

    def test_post_invalid_order4(self):
        order_obj.orders_list.append(self.complete_order)
        order_obj.food_list.clear()
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(resp.status_code, 404)


    def test_post_valid_order_status(self):
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order), content_type='application/json', )
        self.assertEqual(resp.status_code, 201)

    def test_post_invalid_order(self):
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.invalid_order), content_type='application/json', )
        self.assertEqual(resp.status_code, 406)

    def test_post_empty_order(self):
        resp = self.app.post(self.hostname + "orders" )
        self.assertEqual(resp.status_code, 406)

    def test_post_invalid_food_id(self):
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order_invalid_food_id)
                             ,content_type='application/json' )
        self.assertEqual(resp.status_code, 404)


    def tearDown(self):
         order_obj.orders_list.clear()
         self.order_obj.orders_list.clear()
         order_obj.food_list.clear()




if __name__ == "__main__":
    unittest.main()
