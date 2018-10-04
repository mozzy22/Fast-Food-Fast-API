"A module to test get all orders feature"
from tests.base_test import BaseTestCase
class TestPlaceOrder(BaseTestCase):
    "A class for testing the get all orders feature"

    def test_place_orders(self):
        order1 = {
            "order_food_id": 1,
            "order_quantity": 10,}

        order2 = {
            "order_food_id": 2,
            "order_quantity": 10, }

        food = {
            "food_name": "fish",
            "food_price": 22
        }

        food2 = {
            "food_name": "rice",
            "food_price": 22
        }

        invalid_order = {
            "invalid": 1,
            "order_quantity": 10,

        }

        invalid_order_input = {
            "food_name": 2,
            "order_quantity": "",

        }

        # test place order
        self.register_user(self.new_user)
        resp1 = self.login_user(self.resgistered_user)
        token = str(resp1.json["token"])

        #make user admin
        self.make_admin("mos")

        #check list length before post

        resp2 = self.get_all_orders(token)
        self.assertEqual(len(resp2.json), 0)

        #test post oder on empty menu

        resp6 = self.post_order(order1, token)
        self.assertEqual(resp6.status_code, 404)

        #check_list_after post

        self.post_food(food, token)
        self.post_food(food2, token)

        # post orders
        self.post_order(order1,token)
        resp10 = self.post_order(order2, token)
        self.assertEqual(resp10.status_code, 201)

        resp3 = self.get_all_orders(token)
        self.assertEqual(len(resp3.json), 2)
        self.assertEqual(resp3.status_code, 200)

        #test post invalid food object
        resp7 = self.post_order(invalid_order, token)
        self.assertEqual(resp7.status_code, 400)

        #test post invalid input
        resp8 = self.post_order(invalid_order, token)
        self.assertEqual(resp8.status_code, 400)

        #test post existing order
        resp9 = self.post_order(order1, token)
        self.assertEqual(resp9.status_code, 400)







        # resp1 = self.post_food(food, token)
        # self.assertEqual(resp1.status_code, 201)



if __name__ == "__main__":
    unittest.main()
