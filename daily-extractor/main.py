from datetime import datetime
import os
from dotenv import load_dotenv
from flows.services.organizze_service import OrganizzeService, OrganizzeServiceParams
from flows.transactions_extraction import TransactionsExtraction, TransactionsExtractionParams
from prefect.schedules import Cron

load_dotenv()

def schedule_flows():
    
    organizze_service = OrganizzeService(OrganizzeServiceParams(
        base_url=os.getenv("ORGANIZZE_API_URL"), 
        password=os.getenv("ORGANIZZE_PASSWORD"),
        user_agent=os.getenv("ORGANIZZE_USER_AGENT"),
        username=os.getenv("ORGANIZZE_USERNAME")
    ))

    transactions_extraction = TransactionsExtraction(TransactionsExtractionParams(
        organizze_service=organizze_service
    ))

    transactions_extraction.extract.serve(
        name="extract-transactions",
        cron=Cron(
            cron="1 0 * * *",
            timezone="America/Sao_Paulo"
        ),
    )

if __name__ == "__main__":
    schedule_flows()

