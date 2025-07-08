from datetime import datetime
import requests
from typing import TypedDict
from requests.auth import HTTPBasicAuth

from models.category import Category
from models.transaction import Transaction


class OrganizzeServiceParams(TypedDict):
    base_url: str
    username: str
    password: str
    user_agent: str


class GetTransactionsParams(TypedDict):
    from_date: datetime
    to_date: datetime


class OrganizzeService:
    def __init__(self, params: OrganizzeServiceParams) -> None:
        self.__base_url = params.get("base_url")
        self.__auth = HTTPBasicAuth(
            username=params.get("username"), password=params.get("password")
        )
        self.__headers = {"user_agent": params.get("user_agent")}

    def get_transactions(self, params: GetTransactionsParams) -> list[Transaction]:
        start_date = params.get("from_date").strftime("%Y-%m-%d")
        end_date = params.get("to_date").strftime("%Y-%m-%d")

        request_params = {"start_date": start_date, "end_date": end_date}
        response = requests.get(
            f"{self.__base_url}/transactions",
            params=request_params,
            auth=self.__auth,
            headers=self.__headers,
        )

        return response.json()

    def get_category(self, category_id: str) -> Category:
        response = requests.get(
            f"{self.__base_url}/categories/{category_id}",
            auth=self.__auth,
            headers=self.__headers,
        )

        return response.json()
