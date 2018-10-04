from tests.base_test import BaseTestCase

class GetUsers(BaseTestCase):

    def test_get_users(self):
        # test admin can add food

        user = {
            "first_name": "mos",
            "last_name": "mut",
            "user_name": "morrrr",
            "email": "arra@gmail.com",
            "password": "uuuuu6uu"}

        self.register_user(self.new_user)
        resp1 = self.login_user(self.resgistered_user)
        token = str(resp1.json["token"])

        resp0 = self.get_all_users(token)
        self.assertEqual(resp0.status_code, 401)

        # make user admin
        self.make_admin("mos")

        # check list length before post

        resp2 = self.get_all_users(token)
        self.assertEqual(len(resp2.json), 1)
        self.assertEqual(resp2.status_code, 200)

        #register new user
        self.register_user(user)

        resp3 = self.get_all_users(token)
        self.assertEqual(len(resp3.json), 2)
        print(resp3.json)
        self.assertEqual(resp3.status_code, 200)