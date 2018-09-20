import unittest
import json
from app.views.routes import My_app
from app.views.routes import order_obj
from config.config import app_config

class Test_Case(unittest.TestCase):


    def setUp(self):
        " setting up variables to run before test"
        self.hostname = "http://localhost:5000/api/v1/"

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

        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()

    def test_empty_menu_list(self):
        "asserting menu list is empty"
        self.assertEqual(len(order_obj.get_all_foods()),0)

    def test_post_valid_food(self):
         "asserting valid food item aded on a valid post"
         resp = self.app.post(self.hostname + "menu/add", data=json.dumps(self.food),
                              content_type='application/json')
         self.assertEqual(len(order_obj.get_all_foods()), 1)

    def test_post_valid_food2(self):
         "checking status code on a valid post"
         resp = self.app.post(self.hostname + "menu/add", data=json.dumps(self.food),
                              content_type='application/json')
         self.assertEqual(resp.status_code, 201)

    def test_post_invalid_food(self):
         "checking status code on an invalid post"
         resp = self.app.post(self.hostname + "menu/add", data=json.dumps(self.food_invalid),
                              content_type='application/json')
         self.assertEqual(resp.status_code, 406)

    def test_post_exixting_food(self):
        "checking status code on posting existing food item"
        order_obj.food_list.append(self.food)
        resp = self.app.post(self.hostname + "menu/add", data=json.dumps(self.food),
                             content_type='application/json')
        self.assertEqual(resp.status_code, 406)

    def test_post_empty_content(self):
        "checking status code on an empty post"
        order_obj.food_list.append(self.food)
        resp = self.app.post(self.hostname + "menu/add", content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_get_foodlist(self):
        "checking status code on a valid request when menu is empty"
        resp = self.app.get(self.hostname + "menu")
        self.assertEqual(resp.status_code, 200)

    def test_get_foodlist(self):
        "checking status code on a valid request when menu has items"
        order_obj.food_list.append(self.food)
        resp = self.app.get(self.hostname + "menu")
        self.assertEqual(resp.status_code, 202)


    def tearDown(self):
        order_obj.food_list.clear()


if __name__ == "__main__":
    unittest.main()