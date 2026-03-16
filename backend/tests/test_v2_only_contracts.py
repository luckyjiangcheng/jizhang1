import unittest
from pathlib import Path


class TestV2OnlyContracts(unittest.TestCase):
    @staticmethod
    def _project_root() -> Path:
        return Path(__file__).resolve().parents[2]

    def test_frontend_uses_v2_stats_and_budgets(self):
        content = (self._project_root() / "frontend/index.html").read_text(encoding="utf-8")
        self.assertIn("/api/v2/stats/summary", content)
        self.assertIn("/api/v2/stats/trend", content)
        self.assertIn("/api/v2/stats/category", content)
        self.assertIn("/api/v2/budgets/status", content)
        self.assertIn("/api/v2/budgets", content)
        self.assertNotIn("/api/stats/summary", content)
        self.assertNotIn("/api/budgets/status", content)

    def test_frontend_home_removes_v2_only_notice_card(self):
        content = (self._project_root() / "frontend/index.html").read_text(encoding="utf-8")
        self.assertNotIn("仅支持 V2 授权模式", content)
        self.assertNotIn("V2 数据迁移入口", content)

    def test_v2_router_has_stats_and_budget_endpoints(self):
        content = (self._project_root() / "backend/app/api/v2.py").read_text(encoding="utf-8")
        self.assertIn('@router.get("/stats/summary"', content)
        self.assertIn('@router.get("/stats/category"', content)
        self.assertIn('@router.get("/stats/trend"', content)
        self.assertIn('@router.get("/budgets/status"', content)
        self.assertIn('@router.post("/budgets"', content)
        self.assertIn('@router.delete("/budgets/{budget_id}"', content)


if __name__ == "__main__":
    unittest.main()
