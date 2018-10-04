from tests.base_test import BaseTestCase

class test_promote_user(BaseTestCase):

    def test_promote(self):
        #register a new user


        invalid_user = {
        "user_name": "",
        "password": "uuuuu6uu"}

        non_existent_user = {
        "user_name": "ssss",
        "password": "uuuuu6uu"}

        self.register_user(self.new_user)
        resp1 = self.login_user(self.resgistered_user)
        token = str(resp1.json["token"])

        #promote invalid
        resp2 = self.promote_user(invalid_user,token)
        self.assertEqual(resp2.status_code, 400)

        resp3 = self.promote_user(non_existent_user, token)
        self.assertEqual(resp3.status_code, 404)

        resp3 = self.promote_user(self.new_user, token)
        self.assertEqual(resp3.status_code, 200)

