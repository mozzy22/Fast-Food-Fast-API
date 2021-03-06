"A module for testing the add food feature"
import unittest

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

       #invalid key
         invalid_food_obj = {
             "food": "fish",
             "food_price": 22
         }
         #invalid food_price data type
         invalid_food_input = {
             "food_name": "fish",
             "food_price": "gg"
         }

          #invalid  food name
         invalid_food_input1 = {
             "food_name": 2,
             "food_price": "gg"
         }

         #empty food name
         invalid_food_input2 = {
             "food_name": "",
             "food_price": "gg"
         }
         #food name with character
         invalid_food_input3 = {
             "food_name": "fish",
             "food_price": 5
         }

         #test admin can add food
         self.register_user(self.new_user)

         #before user is admin
         resp6 = self.login_user(self.resgistered_user)
         print("this " + str( resp6))
         token = str(resp6.json["token"])
         resp7 = self.post_food(food, token)
         self.assertEqual(resp7.status_code, 401)

         #after user becomes admin
         self.make_admin("mos")
         resp = self.login_user(self.resgistered_user)
         token = str(resp.json["token"])
         resp1 = self.post_food(food ,token)
         self.assertEqual(resp1.status_code, 201)

         #test duplicate food
         resp2 = self.post_food(food, token)
         self.assertEqual(resp2.status_code, 409)

         #test post invalid food
         resp3 = self.post_food(invalid_food_obj, token)
         self.assertEqual(resp3.status_code, 400)

         # test post invalid food input
         resp4 = self.post_food(invalid_food_input, token)
         self.assertEqual(resp4.status_code, 400)

         # test post invalid food input
         resp5 = self.post_food(invalid_food_input1, token)
         self.assertEqual(resp5.status_code, 400)

         # test post invalid food input
         resp6 = self.post_food(invalid_food_input2, token)
         self.assertEqual(resp6.status_code, 400)










if __name__ == "__main__":
    unittest.main()
