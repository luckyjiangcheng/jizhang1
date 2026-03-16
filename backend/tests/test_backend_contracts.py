import unittest
from datetime import datetime

from app.utils.contracts import month_range, normalize_csv_headers, read_csv_value, parse_csv_date, normalize_error_detail


class BackendContractsTest(unittest.TestCase):
    def test_csv_header_compatibility(self):
        row = {"\ufeffDate": "2026-03-10", "Amount": "12.3", "Category": "餐饮美食"}
        normalized = normalize_csv_headers(row)
        self.assertEqual(read_csv_value(normalized, "date", "日期"), "2026-03-10")
        self.assertEqual(read_csv_value(normalized, "amount", "金额"), "12.3")
        self.assertEqual(read_csv_value(normalized, "category", "分类"), "餐饮美食")

    def test_parse_csv_date_supports_multiple_formats(self):
        self.assertEqual(parse_csv_date("2026-03-10"), datetime(2026, 3, 10))
        self.assertEqual(parse_csv_date("2026/03/10"), datetime(2026, 3, 10))
        self.assertEqual(parse_csv_date("2026-03-10T08:30:00"), datetime(2026, 3, 10, 8, 30, 0))

    def test_error_detail_normalization(self):
        self.assertEqual(normalize_error_detail("错误"), "错误")
        self.assertEqual(normalize_error_detail({"detail": "权限不足"}), "权限不足")
        list_detail = [{"loc": ("body", "email"), "msg": "Field required"}]
        self.assertEqual(normalize_error_detail(list_detail), "email: Field required")

    def test_budget_month_range(self):
        start, end = month_range(2026, 2)
        self.assertEqual(start, datetime(2026, 2, 1, 0, 0, 0))
        self.assertEqual(end, datetime(2026, 3, 1, 0, 0, 0))

if __name__ == "__main__":
    unittest.main()
