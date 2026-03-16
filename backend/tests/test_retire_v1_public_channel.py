from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_backend_file(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


class RetireV1PublicChannelSourceTest(unittest.TestCase):
    def test_main_contains_v1_disable_switch_and_migration_response(self):
        content = read_backend_file("main.py")
        self.assertIn("ENABLE_V1_PUBLIC_API", content)
        self.assertIn("status_code=410", content)
        self.assertIn("V1 公共接口已下线，请迁移到 V2 授权通道", content)
        self.assertIn("请改用 /api/v2/* 并携带 X-License-Code 完成授权调用", content)

    def test_main_uses_switch_to_gate_legacy_routers(self):
        content = read_backend_file("main.py")
        self.assertIn("if settings.ENABLE_V1_PUBLIC_API:", content)
        self.assertIn("app.include_router(transactions.router", content)
        self.assertIn("app.include_router(stats.router", content)
        self.assertIn("app.include_router(ai.router", content)
        self.assertIn("app.include_router(version.router", content)
        self.assertIn("app.include_router(budgets.router", content)


class V1RoutersAuthDependencyTest(unittest.TestCase):
    def test_legacy_routers_require_v2_license_dependency(self):
        files = [
            "app/api/transactions.py",
            "app/api/stats.py",
            "app/api/ai.py",
            "app/api/version.py",
            "app/api/budgets.py",
        ]
        for path in files:
            content = read_backend_file(path)
            self.assertIn("router = APIRouter(dependencies=[Depends(get_bound_license_code)])", content)


if __name__ == "__main__":
    unittest.main()
