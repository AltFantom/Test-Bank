import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountDeposit:
    @pytest.mark.parametrize(
        "amount", [1000.0, 1500.9, 9000.0]
    )
    def test_account_deposit_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: float):
        response = api_manager.user_steps.account_deposit_valid(create_user_request, amount)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)

        assert response.balance == amount
        assert account_from_db.balance == amount, "Платеж не прошел"



    @pytest.mark.parametrize(
        "amount", [500.5, 999.5, 9001.5, -500.5]
    )
    def test_account_deposit_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: float):
        response = api_manager.user_steps.account_deposit_invalid(create_user_request, amount)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)

        assert account_from_db.balance == 0, f"Некорректная сумма {account_from_db.balance} поступила на счет"