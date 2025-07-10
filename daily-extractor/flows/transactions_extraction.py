from datetime import datetime
import os
from typing import TypedDict
from prefect import flow, task
from prefect.cache_policies import NO_CACHE
from prefect.logging import get_run_logger

from models.category import Category
from models.transaction import Transaction
from repositories.transactions import TransactionsRepository
from services.organizze_service import (
    GetTransactionsParams,
    OrganizzeService,
    OrganizzeServiceParams,
)


class TransactionsExtractionParams(TypedDict):
    organizze_service: OrganizzeService
    transactions_repository: TransactionsRepository


class TransactionsExtraction:

    def __init__(self, params: TransactionsExtractionParams) -> None:
        self.__organizze_service = params.get("organizze_service")
        self.__transactions_repository = params.get("transactions_repository")

    @task(cache_policy=NO_CACHE)
    def get_transactions_from_range(self, from_date: datetime, to_date: datetime):
        logger = get_run_logger()

        transactions = self.__organizze_service.get_transactions(
            GetTransactionsParams(from_date=from_date, to_date=to_date)
        )
        logger.info(f"{len(transactions)} transactions founded!")

        return transactions

    @task(cache_policy=NO_CACHE)
    def get_transactions_categories(
        self, transactions: list[Transaction]
    ) -> dict[str, Category]:
        categories: dict[str, Category] = {}

        categories_ids = {
            str(transaction.get("category_id")) for transaction in transactions
        }

        for category_id in categories_ids:
            category = self.__organizze_service.get_category(category_id)
            categories[category_id] = category

        return categories

    @task(cache_policy=NO_CACHE)
    def format_transactions(
        self, transactions: list[Transaction], categories: dict[str, Category]
    ):
        return [
            {**transaction, "category": categories[str(transaction.get("category_id"))]}
            for transaction in transactions
        ]

    @task(cache_policy=NO_CACHE)
    def store_transactions(self, transactions):
        logger = get_run_logger()

        ids = self.__transactions_repository.add_transactions(transactions)
        logger.info(f"Stored {len(ids)} transactions")

    def run(self, from_date: datetime, to_date: datetime):
        transactions = self.get_transactions_from_range(from_date, to_date)

        categories = self.get_transactions_categories(transactions)

        transactions = self.format_transactions(transactions, categories)

        self.store_transactions(transactions)


@flow()
def extract():
    logger = get_run_logger()

    logger.info("Initializing flow...")
    organizze_service = OrganizzeService(
        OrganizzeServiceParams(
            base_url=str(os.getenv("ORGANIZZE_API_URL")),
            password=str(os.getenv("ORGANIZZE_PASSWORD")),
            user_agent=str(os.getenv("ORGANIZZE_USER_AGENT")),
            username=str(os.getenv("ORGANIZZE_USERNAME")),
        )
    )

    transactions_repository = TransactionsRepository(db_url=str(os.getenv("DB_URL")))

    transactions_extraction = TransactionsExtraction(
        TransactionsExtractionParams(
            organizze_service=organizze_service,
            transactions_repository=transactions_repository,
        )
    )

    extract_date = datetime.now()
    logger.info(f"Starting extraction for date {extract_date.strftime('%d-%m-%Y')}")
    from_date = extract_date.replace(hour=0, minute=0, second=0, microsecond=0)
    to_date = extract_date.replace(hour=23, minute=59, second=59, microsecond=0)

    transactions_extraction.run(from_date, to_date)
