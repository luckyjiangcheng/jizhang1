import unittest
from pathlib import Path


class Task2RootUserManagementContractsTest(unittest.TestCase):
    @staticmethod
    def _project_root() -> Path:
        return Path(__file__).resolve().parents[2]

    def test_admin_create_user_schema_only_requires_phone_and_account_type(self):
        content = (self._project_root() / "backend/app/schemas.py").read_text(encoding="utf-8")
        section = content.split("class AdminCreateUserRequest(BaseModel):", 1)[1].split("class AdminUserResponse(BaseModel):", 1)[0]
        self.assertIn('phone: str = Field(..., pattern="^1\\\\d{10}$")', section)
        self.assertIn('account_type: str = Field(..., pattern="^(personal|family)$")', section)
        self.assertNotIn("username:", section)
        self.assertNotIn("email:", section)

    def test_admin_create_user_returns_default_password_and_license_count(self):
        content = (self._project_root() / "backend/app/api/admin.py").read_text(encoding="utf-8")
        create_section = content.split('@router.post("/users", response_model=AdminCreateUserResponse', 1)[1].split('@router.get("/license-codes"', 1)[0]
        self.assertIn("initial_password=initial_password", create_section)
        self.assertIn("issued_license_count=license_count", create_section)
        self.assertIn("body: JSON.stringify({ phone, account_type: accountType })", (self._project_root() / "frontend/index.html").read_text(encoding="utf-8"))

    def test_root_users_ui_uses_query_area_and_modal_creation(self):
        content = (self._project_root() / "frontend/index.html").read_text(encoding="utf-8")
        self.assertIn('id="root-user-phone-filter"', content)
        self.assertIn('id="root-user-account-type-filter"', content)
        self.assertIn("onclick=\"openRootCreateUserModal()\"", content)
        self.assertIn('id="root-create-user-modal"', content)
        self.assertIn("showToast(`创建成功，默认密码：${data.initial_password}", content)

    def test_root_users_list_shows_phone_without_tasks_checkbox(self):
        content = (self._project_root() / "frontend/index.html").read_text(encoding="utf-8")
        render_section = content.split("function renderRootUsers(users) {", 1)[1].split("function syncRootUserOptions()", 1)[0]
        self.assertNotIn("<th>Tasks</th>", render_section)
        self.assertNotIn("toggleRootUserTask(", render_section)
        self.assertIn("<th>手机号</th>", render_section)


if __name__ == "__main__":
    unittest.main()
