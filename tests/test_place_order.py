"A module to test the place order feature"
import unittest
import json
from app.models.orders import Orders
from app.views.routes import My_app
from app.views.routes import order_obj
from config.config import app_config

class TestCase(unittest.TestCase):
    "A class to test the place order feature"

    def setUp(self):
        " setting up variables to run before test"
        self.order_obj = Orders()
        self.hostname = "http://localhost:5000/api/v1/"
        self.complete_order = {
            "order_id": 1,
            "order_uuid": 69696969,
            "order_food_id": 3,
            "order_quantity": 3,
            "order_created_at": "12/03/2016",
            "order_status": "pending",
            "order_client": "mutesasira"}

        #valid order to be pasted
        self.order = {
            "order_food_id" : 1,
            "order_quantity" : "1",
            "order_client" :"mutesasira"
        }

       #order with non existent food id
        self.order_invalid_food_id = {
            "order_food_id": 9,
            "order_quantity": "1",
            "order_client": "mutesasira"
        }

       # inalid order format
        self.invalid_order = {
            "order_quantity": "1",
            "order_client": "mutesasira"
        }


        # valid food objet to be posted
        self.food = {
            "food_name": "fish",
            "food_price": "25$"
        }

      #invalid food object to be pasted
        self.food_invalid = {
            "inavlid key": "fish",
            "food_price": "25$"
        }
        order_obj.add_food("pizza", "20$")

        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()

     #testing the model methods
    def test_model_creation(self):
        "A method to test model object creation"
        self.assertIsInstance(self.order_obj, Orders)

    def test_empty_model_oder_list(self):
        "A method to assert no dummy data in mode oredr list"
        self.assertEqual(len(self.order_obj.get_all_orders()), 0)

    def test_place_order(self):
        " a method to assert model place order method"
        self.order_obj.place_order(1, 3, "moses")
        self.assertEqual(len(self.order_obj.get_all_orders()), 1)

    def test_validate_order(self):
        " method to aasert validation of oder order dictionaryobject"
        self.assertFalse(self.order_obj.validate_order_obj(self.invalid_order))

    def test_empty_food_list(self):
        "method to assert empty model food list"
        self.assertEqual(len(self.order_obj.get_all_foods()), 0)

    def test_add_food(self):
        "ethod to assert food added"
        self.order_obj.add_food("pizza", "20$")
        self.assertEqual(len(self.order_obj.get_all_foods()), 1)

    def test_validate_food(self):
        "method to assert valid food dictionary object"
        self.assertTrue(self.order_obj.validate_food_obj(self.food))

    def test_validate_food2(self):
        "method to asert valid invalid food object"
        self.assertFalse(self.order_obj.validate_food_obj(self.food_invalid))


    def test_check_exist_order2(self):
        "method to assert order doesnt exists"
        self.order_obj.place_order(1, 3, "moses")
        self.assertFalse(self.order_obj.check_existing_order(2, "moses"))

    def test_exist_food_id(self):
        "method to assert food id exists"
        self.order_obj.add_food("pizza", "20$")
        self.assertTrue(self.order_obj.check_existing_food(1))

    def test_exist_food_id2(self):
        "method to assert food id doesnt exists"
        self.order_obj.add_food("pizza", "20$")
        self.order_obj.add_food("chicken", "20$")
        self.assertFalse(self.order_obj.check_existing_food(3))

    def test_exist_food_name(self):
        "method to assert food exists byname"
        self.order_obj.add_food("pizza", "20$")
        self.assertTrue(self.order_obj.check_existing_food("pizza"))

    def test_exist_food_name2(self):
        "method to assert food  doesnt exist by name"
        self.order_obj.add_food("pizza", "20$")
        self.assertFalse(self.order_obj.check_existing_food("none"))

#Testing the routes
    def test_empty_list(self):
        "method to assert empty order objct"
        self.assertEqual(len(order_obj.get_all_orders()), 0)

    def test_post_valid_order(self):
        "testing valid order is added to order list"
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order),
                             content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 1)
        print(str(resp.data))

    def test_post_valid_order2(self):
        "testing valid order is added to order list"
        order_obj.orders_list.append(self.complete_order)
        self.app.post(self.hostname + "orders", data=json.dumps(self.order),
                      content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 2)

    def test_post_invalid_order(self):
        "testing object list if invalid order is posted"
        order_obj.orders_list.append(self.complete_order)
        self.app.post(self.hostname + "orders", data=json.dumps(self.invalid_order),
                      content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 1)

    def test_post_invalid_order1(self):
        "testing valid order is posted wen food list is empty"
        order_obj.orders_list.append(self.complete_order)
        order_obj.food_list.clear()
        self.app.post(self.hostname + "orders", data=json.dumps(self.order),
                      content_type='application/json')
        self.assertEqual(len(order_obj.get_all_orders()), 1)

    def test_post_invalid_order4(self):
        "testing status code if valid order posted wen food list is empty"
        order_obj.orders_list.append(self.complete_order)
        order_obj.food_list.clear()
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order),
                             content_type='application/json')
        self.assertEqual(resp.status_code, 200)


    def test_post_valid_order_status(self):
        "testing status code if valid order is posted"
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order),
                             content_type='application/json', )
        self.assertEqual(resp.status_code, 201)

    def test_post_invalid_order2(self):
        "testing status code if invalid order is posted"
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.invalid_order),
                             content_type='application/json', )
        self.assertEqual(resp.status_code, 406)


    def test_post_invalid_food_id(self):
        "testing status code if order with non existent food id is posted"
        resp = self.app.post(self.hostname + "orders", data=json.dumps(self.order_invalid_food_id)
                             , content_type='application/json')
        self.assertEqual(resp.status_code, 200)


    def tearDown(self):
        "clearing the object lists after test runs"
        order_obj.orders_list.clear()
        self.order_obj.orders_list.clear()
        order_obj.food_list.clear()




if __name__ == "__main__":
    unittest.main()
