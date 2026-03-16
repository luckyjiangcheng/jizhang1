import unittest
from pathlib import Path


class PhoneLoginContractsTest(unittest.TestCase):
    @staticmethod
    def _project_root() -> Path:
        return Path(__file__).resolve().parents[2]

    def test_user_login_schema_uses_phone(self):
        content = (self._project_root() / "backend/app/schemas.py").read_text(encoding="utf-8")
        user_login_section = content.split("class UserLogin(BaseModel):", 1)[1].split("class UserResponse(BaseModel):", 1)[0]
        self.assertIn('phone: str = Field(..., pattern="^1\\\\d{10}$")', user_login_section)
        self.assertNotIn("email: EmailStr", user_login_section)

    def test_auth_login_queries_phone_and_hides_account_existence(self):
        content = (self._project_root() / "backend/app/api/auth.py").read_text(encoding="utf-8")
        login_section = content.split('@router.post("/login", response_model=Token)', 1)[1].split('@router.get("/me", response_model=UserResponse)', 1)[0]
        self.assertIn("User.phone == user_data.phone", login_section)
        self.assertIn('detail="手机号或密码错误"', login_section)
        self.assertNotIn("User.email == user_data.email", login_section)
        self.assertNotIn('detail="邮箱或密码错误"', login_section)

    def test_frontend_login_uses_phone_field(self):
        content = (self._project_root() / "frontend/index.html").read_text(encoding="utf-8")
        self.assertIn('id="login-phone"', content)
        self.assertIn("JSON.stringify({ phone: account, password })", content)
        self.assertNotIn('id="login-email"', content)
        self.assertNotIn("JSON.stringify({ email, password })", content)


if __name__ == "__main__":
    unittest.main()
