import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize(
        "amount, term_months", [
            (5500, 12)
        ]
    )
    def test_credit_repay_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_credit_request,
            create_credit_account,
            amount,
            term_months
    ):
        response = api_manager.credit.credit_repay_valid(create_credit_request, create_credit_account, amount, term_months)
        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db.balance == 0
        assert response.amountDeposited == amount


    @pytest.mark.parametrize(
        "amount, term_months", [
            (5500, 12)
        ]
    )
    def test_credit_repay_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_credit_request,
            create_credit_account,
            amount,
            term_months
    ):
        credit_id = api_manager.credit.credit_repay_invalid(
            create_credit_request,
            create_credit_account,
            amount,
            term_months
        )
        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_id)
        assert credit_from_db.balance == amount
