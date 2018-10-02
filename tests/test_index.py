"A module for testing the add food feature"
import unittest
import json
from tests.base_test import BaseTestCase
from app.views.menu_blueprint import order_obj


class TestGetIndex(BaseTestCase):
    "The test Class for the add_food feature"

    def test_get_index_page(self):
        resp = self.app.get("http://localhost:5000/")
        self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()
