from pymongo import MongoClient


class TransactionsRepository:

    def __init__(self, db_url: str) -> None:
        self.__client = MongoClient(db_url)
        self.__db = self.__client["my-finances"]

    def add_transactions(self, transactions) -> list[str]:
        transactions_collection = self.__db["transactions"]
        result = transactions_collection.insert_many(transactions)
        return result.inserted_ids
