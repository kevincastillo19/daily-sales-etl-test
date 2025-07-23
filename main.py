import argparse

from app.core.etl import ProcessorETL
from app.config.db import Database
from app.config.logger import Logger


def main(filepath: str):
    logger = Logger("sales-etl")
    db = Database()
    etl = ProcessorETL(db, logger)
    data = etl.extract(filepath)
    transformed_data = etl.transform(data)
    etl.load(transformed_data)
    logger.log_info("ETL process completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the sales ETL process.")
    parser.add_argument("--source", required=True, help="Path to the CSV file")
    args = parser.parse_args()
    main(args.source)
