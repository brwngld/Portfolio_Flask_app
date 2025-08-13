import unittest

from app import create_app


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Portfolio", response.data)

    def test_about_page(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About", response.data)

    def test_contact_page(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contact", response.data)


if __name__ == "__main__":
    unittest.main()
