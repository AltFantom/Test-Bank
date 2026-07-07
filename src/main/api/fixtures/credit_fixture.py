import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_credit_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditRequest)
    create_user_request = CreateUserRequest(
            username=user_request.username,
            password=user_request.password,
            role=user_request.role
        )
    api_manager.admin_steps.create_user(
        create_user_request
    )
    return create_user_request

@pytest.fixture
def create_credit_account(api_manager, create_credit_request):
    def account():
        return api_manager.user_steps.create_account_valid(create_credit_request)
    return account
