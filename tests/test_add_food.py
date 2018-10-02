"A module for testing the add food feature"
import unittest
import json
from tests.base_test import BaseTestCase
from app.views.menu_blueprint import order_obj


class TestCase(BaseTestCase):
    "The test Class for the add_food feature"


    def test_empty_menu_list(self):
        "asserting menu list is empty"
        self.assertEqual(len(order_obj.get_all_foods()), 0)

    def test_add_food(self):
         food = {
             "food_name": "fish",
             "food_price": 22
         }

         invalid_food_obj = {
             "food": "fish",
             "food_price": 22
         }
         invalid_food_input = {
             "food": "fish",
             "food_price": "gg"
         }



         #test admin can add food
         self.register_user(self.new_user)

         #before user is admin
         resp6 = self.login_user(self.resgistered_user)
         token = str(resp6.json["token"])
         resp7 = self.post_food(food, token)
         self.assertEqual(resp7.status_code, 401)

         #after user becomes admin
         self.make_admin("mo1")
         resp = self.login_user(self.resgistered_user)
         token = str(resp.json["token"])
         resp1 = self.post_food(food ,token)
         self.assertEqual(resp1.status_code, 201)

         #test duplicate food
         resp2 = self.post_food(food, token)
         self.assertEqual(resp2.status_code, 400)

         #test post invalid food
         resp3 = self.post_food(invalid_food_obj, token)
         self.assertEqual(resp3.status_code, 400)

         # test post invalid food input
         resp4 = self.post_food(food, token)
         self.assertEqual(resp4.status_code, 400)








if __name__ == "__main__":
    unittest.main()
