import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountTransfer:
    MAX_AMOUNT_DEPOSIT = 9000.0
    @pytest.mark.parametrize(
        "amount", [500, 5555.5, 10000.0]
    )
    def test_account_transfer_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            create_user_account,
            amount: float
    ):
        response = api_manager.user_steps.account_transfer_valid(create_user_account, create_user_request, amount, self.MAX_AMOUNT_DEPOSIT)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.fromAccountId)

        assert response.fromAccountIdBalance == self.MAX_AMOUNT_DEPOSIT * 2 - amount
        assert account_from_db.balance == self.MAX_AMOUNT_DEPOSIT * 2 - amount

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
        account_from_id = api_manager.user_steps.account_transfer_invalid(create_user_account, create_user_request, amount)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_from_id)

        assert account_from_db.balance == 0

