from dotenv import load_dotenv
from flows.transactions_extraction import (
    extract,
)
from prefect.schedules import Cron

load_dotenv()


def schedule_flows():
    extract.serve(
        name="extract-transactions",
        schedule=Cron("1 0 * * *", timezone="America/Sao_Paulo"),
    )


if __name__ == "__main__":
    schedule_flows()
