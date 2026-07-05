from typing import Optional

import requests
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HTTPRequester
from src.main.api.models.base_model import BaseModel
import allure


class CrudRequester(HTTPRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body,
        )

        allure.attach(str(body), "Response body", allure.attachment_type.JSON)

        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response