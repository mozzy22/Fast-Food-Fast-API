"A module to test get all orders feature"
import uuid
from tests.base_test import BaseTestCase
class TestGetOrdersHistory(BaseTestCase):
    "A class for testing the get all orders feature"

    def test_order_history(self):
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

        # test admin can add food
        self.register_user(self.new_user)
        resp1 = self.login_user(self.resgistered_user)
        token = str(resp1.json["token"])

        resp0 = self.get_all_orders(token)
        self.assertEqual(resp0.status_code, 401)

        #make user admin
        self.make_admin("mos")

        #check list length before post


        resp2 = self.get_all_orders(token)
        self.assertEqual(len(resp2.json), 0)



        #check_list_after post

        self.post_food(food, token)
        self.post_food(food2, token)


        #check order history before posting

        resp6 = self.get_user_order_history(token)
        self.assertEqual(len(resp6.json), 0)

        # post orders
        self.post_order(order1,token)
        resp4 = self.post_order(order2, token)


        #test get user order history after posting
        resp7 = self.get_user_order_history(token)
        self.assertEqual(len(resp7.json), 2)
        self.assertEqual(resp7.status_code, 200)






if __name__ == "__main__":
    unittest.main()
