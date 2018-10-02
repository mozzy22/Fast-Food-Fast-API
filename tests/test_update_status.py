"A module to test get all orders feature"
import uuid
from tests.base_test import BaseTestCase
class TestGetOrders(BaseTestCase):
    "A class for testing the get all orders feature"

    def test_update_statu(self):

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
        status1 = {"order_status": "ok"}
        status2 = {"order_status": "yes"}
        status3 = {"order_status": "no"}
        unknown_status1 = {"order_status": "not sure"}
        invalidstatus1 = {"order_status": 2}
        invalid_status_object = {"order": "ok"}
        empty_status = {"order": ""}



        # test admin can add food
        self.register_user(self.new_user)
        resp1 = self.login_user(self.resgistered_user)
        token = str(resp1.json["token"])

        #make user admin
        self.make_admin("mo1")

        #check list length before post

        resp2 = self.get_all_orders(token)
        self.assertEqual(len(resp2.json), 0)

        #check_list_after post

        self.post_food(food, token)
        self.post_food(food2, token)

        # post orders
        self.post_order(order1,token)
        resp4 = self.post_order(order2, token)
        uuid_1 = resp4.json["order_uuid"]

        #test update specific order
        resp5 = self.update_status(status1, uuid_1,token)
        self.assertEqual(resp5.status_code, 200)

        resp6 = self.update_status(status2, uuid_1, token)
        self.assertEqual(resp6.status_code, 200)

        resp7 = self.update_status(status3, uuid_1, token)
        self.assertEqual(resp7.status_code, 200)

        resp8 = self.update_status(unknown_status1, uuid_1, token)
        self.assertEqual(resp8.status_code, 200)

        resp9 = self.update_status(invalid_status_object, uuid_1, token)
        self.assertEqual(resp9.status_code, 400)

        resp10 = self.update_status(invalidstatus1, uuid_1, token)
        self.assertEqual(resp10.status_code, 400)

        resp11 = self.update_status(empty_status, uuid_1, token)
        self.assertEqual(resp11.status_code, 400)

        #test fetch order which doent exist
        uuid_2 = uuid.uuid1()
        resp12 = self.update_status(status1, uuid_2, token)
        self.assertEqual(resp12.status_code, 400)







        # resp1 = self.post_food(food, token)
        # self.assertEqual(resp1.status_code, 201)



if __name__ == "__main__":
    unittest.main()
