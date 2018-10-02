"A module for testing the add food feature"
import unittest
import json
from tests.base_test import BaseTestCase
from app.views.menu_blueprint import order_obj


class TestGetMenu(BaseTestCase):
    "The test Class for the add_food feature"


    def test_empty_menu_list(self):
        "asserting menu list is empty"
        self.assertEqual(len(order_obj.get_all_foods()), 0)

    def test_add_food(self):
         food = {
             "food_name": "fish",
             "food_price": 22
         }
         food2 = {
             "food_name": "rice",
             "food_price": 22
         }

         #test admin can add food

         self.register_user(self.new_user)

         #after user becomes admin
         self.make_admin("mo1")
         resp = self.login_user(self.resgistered_user)
         token = str(resp.json["token"])

         #fetch menu before post

         resp2 = self.get_menu(token)
         self.assertEqual(len(resp2.json), 0)

         #post food to menu
         self.post_food(food ,token)
         self.post_food(food2,token)

        #test fetch menu after add

         resp3 = self.get_menu(token)
         self.assertEqual(len(resp3.json), 2)
         self.assertEqual(resp3.status_code, 200)













if __name__ == "__main__":
    unittest.main()
