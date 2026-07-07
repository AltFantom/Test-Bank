from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response import AccountTransferResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    @staticmethod
    def create_account_valid(create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_created(),
        ).post()
        return response

    @staticmethod
    def create_account_invalid(create_user_request: CreateUserRequest):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_conflict(),
        ).post()
        return response

    @staticmethod
    def account_deposit_valid(create_user_account: CreateUserResponse, create_user_request: CreateUserRequest, amount: float):
        account_deposit_request = AccountDepositRequest(
            accountId=create_user_account.id,
            amount=amount
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            response_spec=ResponseSpecs.request_ok(),
        ).post(account_deposit_request)
        return response

    @staticmethod
    def account_deposit_invalid(create_user_account,  create_user_request: CreateUserRequest, amount: float):
        user_acc = create_user_account()
        account_deposit_request = AccountDepositRequest(
            accountId=user_acc.id,
            amount=amount
        )
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            response_spec=ResponseSpecs.request_bad(),
        ).post(account_deposit_request)
        return user_acc

    def account_transfer_valid(self, create_user_account, create_user_request: CreateUserRequest, amount: float, deposit_amount) -> AccountTransferResponse:
        first_account = create_user_account()
        self.account_deposit_valid(first_account, create_user_request, deposit_amount)
        self.account_deposit_valid(first_account, create_user_request, deposit_amount)
        second_account = create_user_account()
        account_transfer_request = AccountTransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=amount
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            response_spec=ResponseSpecs.request_ok(),
        ).post(account_transfer_request)
        return response

    @staticmethod
    def account_transfer_invalid(create_user_account, create_user_request: CreateUserRequest, amount: float):
        first_account = create_user_account()
        second_account = create_user_account()
        account_transfer_request = AccountTransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=amount
        )
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            response_spec=ResponseSpecs.request_unprocessable_content(),
        ).post(account_transfer_request)
        return first_account.id
