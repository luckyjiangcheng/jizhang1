import unittest
from app.utils.license_codes import generate_license_code, is_installable_status, is_callable_status


class LicenseCodeUtilsTest(unittest.TestCase):
    def test_generate_license_code_format(self):
        code = generate_license_code("fixed-seed")
        self.assertTrue(code.startswith("LC-"))
        self.assertEqual(len(code), 15)

    def test_generate_license_code_changes_with_seed(self):
        code_a = generate_license_code("seed-a")
        code_b = generate_license_code("seed-b")
        self.assertNotEqual(code_a, code_b)

    def test_status_checks(self):
        self.assertTrue(is_installable_status("unused"))
        self.assertFalse(is_installable_status("used"))
        self.assertFalse(is_callable_status("unused"))
        self.assertTrue(is_callable_status("used"))


if __name__ == "__main__":
    unittest.main()
