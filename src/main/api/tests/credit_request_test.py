import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize(
        "amount, term_months", [
            (5500, 12)
        ]
    )
    def test_credit_request_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_credit_request,
            create_credit_account,
            amount: float,
            term_months: int
    ):
        account = create_credit_account()
        response = api_manager.credit.credit_request_valid(create_credit_request, account, amount, term_months)
        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db.balance == amount, "Отсутствует счет в БД, либо баланс не совпадает с запрошенным"
        assert response.balance == amount, "запрошенный кредит не соответствует фактическому"

    @pytest.mark.parametrize(
        "amount, term_months", [
            (5500, 12)
        ]
    )
    def test_credit_request_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_credit_request,
            create_credit_account,
            amount: float,
            term_months: int
    ):
        response = api_manager.credit.credit_request_invalid(create_credit_request, create_credit_account, amount, term_months)
        credit_from_db = CreditCrudDb.get_credits_by_account_id(db_session, response.id)

        assert credit_from_db is None, f"При невалидном запросе выдался кредит по account_id = {response.id}"