import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountTransfer:
    @pytest.mark.parametrize(
        "amount, deposit", [
            (500, 2000.0),
            (5555.5, 4000),
            (10000.0, 6000)
        ]
    )
    def test_account_transfer_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            create_user_account,
            amount: float,
            deposit: float
    ):
        response = api_manager.user_steps.account_transfer_valid(create_user_account, create_user_request, amount, deposit)
        to_account_from_db = AccountCrudDb.get_account_by_id(db_session, response.toAccountId)

        assert to_account_from_db.balance == amount, f"Деньги не пришли на счет с id = {to_account_from_db.id}"

    @pytest.mark.parametrize(
        "amount", [1500, 2500]
    )
    def test_account_transfer_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            create_user_account,
            amount: float
    ):
        account_to_id = api_manager.user_steps.account_transfer_invalid(create_user_account, create_user_request, amount)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_to_id)

        assert account_from_db.balance == 0, f"С нулевого баланса ушли деньги"

