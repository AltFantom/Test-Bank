import pytest
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(
            username="admin", password="123456"
        )

        response = api_manager.admin_steps.login_user(login_user_request)

        assert response.user.username == login_user_request.username, f"Пользователь создался с другим username, ожидался - {login_user_request.username}, по факту - {response.username}"
        assert response.user.role == "ROLE_ADMIN", "Пользователь создался с другой ролью, ожидалась - ROLE_ADMIN, по факту - {response.user.role}"

    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, f"Пользователь создался с другим username, ожидался - {create_user_request.username}, по факту - {response.user.username}"
        assert response.user.role == "ROLE_USER", "Пользователь создался с другой ролью, ожидалась - ROLE_USER, по факту - {response.user.role}"