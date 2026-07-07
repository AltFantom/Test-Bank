from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.creadit_repay_request import CreditRepayRequest
from src.main.api.models.creadit_repay_response import CreditRepayResponse
from src.main.api.models.creadit_request_request import CreditRequestRequest
from src.main.api.models.creadit_request_respone import CreditRequestResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class CreditSteps(BaseSteps):
    @staticmethod
    def credit_request_valid(
            create_credit_request,
            account,
            amount: float,
            term_months: int
    ) -> CreditRequestResponse:
        credit_request_request = CreditRequestRequest(
            accountId=account.id,
            amount=amount,
            termMonths=term_months
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_credit_request.username,
                                                   create_credit_request.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_created(),
        ).post(credit_request_request)
        return response

    @staticmethod
    def credit_request_invalid(
            create_credit_request,
            create_credit_account,
            amount: float,
            term_months: int
    ) -> CreateAccountResponse:
        first_account = create_credit_account()
        credit_request_request = CreditRequestRequest(
            accountId=first_account.id,
            amount=amount,
            termMonths=term_months
        )
        ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_credit_request.username,
                                                   create_credit_request.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_created(),
        ).post(credit_request_request)
        second_account = create_credit_account()
        credit_request_request = CreditRequestRequest(
            accountId=second_account.id,
            amount=amount,
            termMonths=12
        )
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(create_credit_request.username,
                                                   create_credit_request.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_forbidden(),
        ).post(credit_request_request)
        return second_account

    def credit_repay_valid(
            self,
            create_credit_request,
            create_credit_account,
            amount: float,
            term_months: int
    ) -> CreditRepayResponse:
        account = create_credit_account()
        credit_request_response = self.credit_request_valid(create_credit_request, account, amount, term_months)
        credit_repay_request = CreditRepayRequest(
            creditId=credit_request_response.creditId,
            accountId=account.id,
            amount=amount,
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                create_credit_request.username,
                create_credit_request.password
            ),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.request_ok(),
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid(
            self,
            create_credit_request,
            create_credit_account,
            amount: float,
            term_months: int
    ) -> int:
        account = create_credit_account()
        credit_request_response = self.credit_request_valid(
            create_credit_request,
            account,
            amount,
            term_months
        )
        credit_repay_request = CreditRepayRequest(
            creditId=credit_request_response.creditId,
            accountId=account.id,
            amount=amount*2,
        )
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                create_credit_request.username,
                create_credit_request.password
            ),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.request_unprocessable_content(),
        ).post(credit_repay_request)
        return credit_request_response.creditId
