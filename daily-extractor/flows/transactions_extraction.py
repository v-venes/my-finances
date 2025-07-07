from datetime import datetime
import os
from typing import TypedDict
from prefect import flow, task
from prefect.logging import get_run_logger

from flows.services.organizze_service import (
    GetTransactionsParams,
    OrganizzeService,
    OrganizzeServiceParams,
)


class TransactionsExtractionParams(TypedDict):
    organizze_service: OrganizzeService


class TransactionsExtraction:

    def __init__(self, params: TransactionsExtractionParams) -> None:
        self.__organizze_service = params.get("organizze_service")

    # Passar repository

    @task
    def get_transactions_from_range(self, from_date: datetime, to_date: datetime):
        logger = get_run_logger()

        transactions = self.__organizze_service.get_transactions(
            GetTransactionsParams(from_date=from_date, to_date=to_date)
        )
        logger.info(f"{len(transactions)} transactions founded!")

        return transactions

    @task
    def get_transactions_categories(self, transactions) -> list[str]:
        return []

    @task
    def format_transactions(self, transactions, categories):
        return []

    @task
    def store_transactions(self, transactions):
        pass

    def run(self, from_date: datetime, to_date: datetime):
        transactions = self.get_transactions_from_range(from_date, to_date)

        self.store_transactions(transactions)


@flow()
def extract():
    logger = get_run_logger()

    logger.info("Initializing flow...")
    organizze_service = OrganizzeService(
        OrganizzeServiceParams(
            base_url=os.getenv("ORGANIZZE_API_URL"),
            password=os.getenv("ORGANIZZE_PASSWORD"),
            user_agent=os.getenv("ORGANIZZE_USER_AGENT"),
            username=os.getenv("ORGANIZZE_USERNAME"),
        )
    )

    transactions_extraction = TransactionsExtraction(
        TransactionsExtractionParams(organizze_service=organizze_service)
    )

    extract_date = datetime.now()
    logger.info(f"Starting extraction for date {extract_date.strftime("%d/%m/%Y")}")
    from_date = extract_date.replace(hour=0, minute=0, second=0, microsecond=0)
    to_date = extract_date.replace(hour=23, minute=59, second=59, microsecond=0)

    transactions_extraction.run(from_date, to_date)
