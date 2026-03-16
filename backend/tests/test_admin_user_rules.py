import unittest

from app.utils.admin_user_rules import is_valid_phone, build_initial_password


class AdminUserRulesTest(unittest.TestCase):
    def test_phone_validation_rejects_invalid_phone(self):
        self.assertFalse(is_valid_phone("1380013800"))
        self.assertFalse(is_valid_phone("23800138000"))
        self.assertFalse(is_valid_phone("1380013800a"))

    def test_phone_validation_accepts_11_digit_phone(self):
        self.assertTrue(is_valid_phone("13800138000"))

    def test_initial_password_uses_last_6_digits_of_phone(self):
        self.assertEqual(build_initial_password("13800138000"), "138000")

    def test_initial_password_raises_for_invalid_phone(self):
        with self.assertRaises(ValueError):
            build_initial_password("1380013800")


if __name__ == "__main__":
    unittest.main()
