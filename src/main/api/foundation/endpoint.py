from enum import Enum
from typing import Optional, Type

from dataclasses import dataclass

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response import AccountTransferResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.creadit_repay_request import CreditRepayRequest
from src.main.api.models.creadit_repay_response import CreditRepayResponse
from src.main.api.models.creadit_request_request import CreditRequestRequest
from src.main.api.models.creadit_request_respone import CreditRequestResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    ACCOUNT_DEPOSIT = EndpointConfiguration(
        request_model=AccountDepositRequest,
        url="/account/deposit",
        response_model=AccountDepositResponse
    )

    ACCOUNT_TRANSFER = EndpointConfiguration(
        request_model=AccountTransferRequest,
        url="/account/transfer",
        response_model=AccountTransferResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model=CreditRequestRequest,
        url="/credit/request",
        response_model=CreditRequestResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model=CreditRepayRequest,
        url="/credit/repay",
        response_model=CreditRepayResponse
    )