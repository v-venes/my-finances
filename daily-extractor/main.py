from datetime import datetime
import random

from dotenv import load_dotenv
from prefect import flow, task
from flows.transactions_extraction import TransactionsExtraction
from prefect.schedules import Cron

load_dotenv()

def schedule_flows():
    TransactionsExtraction().extract.serve(
        name="extract-transactions",
        cron=Cron(
            cron="1 0 * * *",
            timezone="America/Sao_Paulo"
        ),
    )

if __name__ == "__main__":
    # schedule_flows()
    current_date = datetime.now()
    #TransactionsExtraction().extract(current_date)

