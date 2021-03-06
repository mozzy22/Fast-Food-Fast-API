"A module for testing the add food feature"
import unittest

from tests.base_test import BaseTestCase


class TestGetIndex(BaseTestCase):
    "The test Class for the add_food feature"

    def test_get_index_page(self):
        resp = self.app.get("http://localhost:5000/index")
        self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()
