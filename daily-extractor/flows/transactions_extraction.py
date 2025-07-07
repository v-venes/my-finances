from datetime import datetime
from typing import TypedDict
from prefect import flow, task
from prefect.logging import get_run_logger

from flows.services.organizze_service import GetTransactionsParams, OrganizzeService

class TransactionsExtractionParams(TypedDict):
    organizze_service: OrganizzeService

class TransactionsExtraction:
    

    def __init__(self, params: TransactionsExtractionParams) -> None:
        self.__organizze_service = params.get("organizze_service")
    # Passar repository

    @task
    def get_transactions_from_range(self, from_date: datetime, to_date: datetime):
        logger = get_run_logger()

        transactions = self.__organizze_service.get_transactions(GetTransactionsParams(from_date=from_date, to_date=to_date))
        logger.info(f"{len(transactions)} transactions founded!")
        print(transactions)
        return []

    @task
    def store_transactions(self, transactions):
        pass

    @flow()
    def extract(self):
        logger = get_run_logger()
        extract_date = datetime.now()
        logger.info(f"Starting extraction for date {extract_date}")
        from_date = extract_date.replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = extract_date.replace(hour=23, minute=59, second=59, microsecond=0)

        transactions = self.get_transactions_from_range(from_date, to_date)

        self.store_transactions(transactions)
