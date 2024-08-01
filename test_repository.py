import unittest
from fastapi import HTTPException
from app.routes import register, users_db

class TestUserRepository(unittest.TestCase):

    def setUp(self):
        users_db.clear()

    def test_register_user(self):
        email = "test@example.com"
        password = "testpassword"
        response = register(email, password)
        self.assertEqual(response, {"msg": "Please verify your email"})
        self.assertIn(email, users_db)

    def test_register_existing_user(self):
        email = "existing@example.com"
        password = "testpassword"
        users_db[email] = {"email": email, "password": password}
        with self.assertRaises(HTTPException) as context:
            register(email, password)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "User already exists")

if __name__ == "__main__":
    unittest.main()
