#!/usr/bin/env python3
import unittest
from app import app  # import the Flask app instance from app.py

class ItemsApiTestCase(unittest.TestCase):
    def set_up(self):
        # Runs before each test. Set up a test client for our Flask app.
        app.testing = True # put Flask in testing mode
        self.client = app.test_client()

    def test_get_items_status_code(self):
        """GET /items should respond with HTTP 200 OK."""
        response = self.client.get("/items")
        # response = self.get("/items")
        self.assertEqual(response.status_code, 200)

    def test_get_items_returns_list(self):
        """GET /items should return a JSON list of items."""
        response = self.client.get("/items")
        # response = self.get("/items")
        data = response.get_json()
        # Verify that the response is a list
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_items_have_id_and_name(self):
        """Each item in the list should have 'id' and 'name' fields."""
        response = self.client.get("/items")
        # response = self.get("/items")
        data = response.get_json()
        if len(data) > 0:
            item = data[0]
            self.assertIsInstance(item, dict)
            self.assertIn("id", item)
            self.assertIn("name", item)

    def test_sample_item_present(self):
        """The default 'Sample Item 1' should be part of the response."""
        response = self.client.get("/items")
        # response = self.get("/items")
        data = response.get_json()
        names = [item["name"] for item in data]
        self.assertIn("Sample Item 1", names)

if __name__ == "__main__":
    unittest.main()
