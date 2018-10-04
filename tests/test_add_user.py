from tests.base_test import BaseTestCase
import unittest


class MyTestCase(BaseTestCase):

    def test_register_user(self):
        user = {
            "first_name": "moses",
            "last_name": "mut",
            "user_name": "mos",
            "email": "aa@gmail.com",
            "password": "uuuuu6uu"}

        invalid_user = {
            "first_name": "moses",
            "user_name": "mos",
            "email": "aa@gmail.com",
            "password": "uuuuu6uu"}

        invalid_user_input = {
            "first_name": "",
            "last_name": "",
            "user_name": "mos",
            "email": "aa@gmail.com",
            "password": "uuuuu6uu"}

        invalid_user_pass = {
            "first_name": "moses",
            "last_name": "mut",
            "user_name": "mos",
            "email": "aa@gmail.com",
            "password": "wwww"}

        invalid_user_email = {
            "first_name": "moses",
            "last_name": "mut",
            "user_name": "mos",
            "email": "gmail",
            "password": "uuuuu6uu"}

        #test regiter a valid user
        resp1 = self.register_user(user)
        self.assertEqual(resp1.status_code, 201)

        # test regiter a invlid_  user object
        resp2 = self.register_user(invalid_user)
        self.assertEqual(resp2.status_code, 400)

        # test regiter a invalid user inout
        resp3 = self.register_user(invalid_user_input)
        self.assertEqual(resp3.status_code, 400)

        # test regiter a invalid email
        resp4 = self.register_user(invalid_user_email)
        self.assertEqual(resp4.status_code, 400)

        # test regiter a invalid input
        resp5 = self.register_user(invalid_user_input)
        self.assertEqual(resp5.status_code, 400)

        resp5 = self.register_user(invalid_user_pass)
        self.assertEqual(resp5.status_code, 400)

        # test regiter an existing user
        resp6 = self.register_user(user)
        self.assertEqual(resp6.status_code, 409)


    def test_login_user(self):
        user = {
            "first_name": "moses",
            "last_name": "mut",
            "user_name": "mos",
            "email": "aa@gmail.com",
            "password": "uuuuu6uu"}

        login_user = {
        "user_name": "mos",
        "password": "uuuuu6uu"  }

        login_invalid_user = {
            "user_name": "mozzy",
            "password": "uuuuu6uu"}

        login_invalid_user_obj = {
            "user": "mozzy",
            "password": "uuuuu6uu"}

        login_invalid_user_input = {
            "user": "",
            "password": "uuuuu6uu"}

        #test valid login
        self.register_user(user)
        resp1 = self.login_user(login_user)
        self.assertEqual(resp1.status_code, 200)

        #test invalid login
        resp2 = self.login_user(login_invalid_user)
        self.assertEqual(resp2.status_code, 401)

        resp3 = self.login_user(login_invalid_user_obj)
        self.assertEqual(resp3.status_code, 400)

        resp4 = self.login_user(login_invalid_user_input)
        self.assertEqual(resp4.status_code, 400)


if __name__ == '__main__':
    unittest.main()
