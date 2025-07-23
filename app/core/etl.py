import os
import pandas as pd  # type: ignore # pylint: disable=import-error
from app.config.db import Database
from app.config.logger import Logger


class ProcessorETL:
    def __init__(self, db_connection: Database, logger: Logger):
        """
        Initialize the ProcessorETL class.

        :param db_connection: Database connection object.
        :param logger: Logger object for logging.
        """
        self.db_connection = db_connection
        self.logger = logger
        self.source = None

    def _validate_filepath(self, filepath: str):
        """
        Validate the provided file path.

        :param filepath: Path to the CSV file.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Invalid file path provided.")
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"The file {filepath} does not exist.")

    def extract(self, filepath: str):
        """
        Load the provided data into the database.

        :param filepath: Path to the CSV file to be loaded.
        """
        self.logger.log_info("Starting data extraction process.")
        self.source = filepath
        self.logger.log_info(f"Extracting data from: {self.source}")
        return pd.read_csv(filepath, sep=";", encoding="utf-8")

    def transform(self, data: pd.DataFrame):
        """
        Transform the data by converting the 'date' column to datetime format.

        :param df: DataFrame containing the data to be transformed.
        """
        try:
            self.logger.log_info("Starting data transformation process.")
            data["date"] = pd.to_datetime(data["date"])
            data["customer_name"] = data["customer_name"].str.strip()
            conversion_rates = {"USD": 1, "EUR": 1.2, "COP": 0.00025}
            data["amount"] = data.apply(
                lambda row: round(
                    row["amount"] * conversion_rates.get(row["currency"], 1), 2
                ),
                axis=1,
            )
            data["file"] = self.source  # Source file related
            self.logger.log_info(
                f"({self.source}) - Data transformation completed successfully."
            )
            return data
        except Exception as e:
            self.logger.log_error(e)
            raise

    def load(self, data: pd.DataFrame):
        """
        Load the transformed data into the database.

        :param df: DataFrame containing the data to be loaded.
        """
        try:
            self.logger.log_info(f"({self.source}) - Starting data loading process.")
            data.to_sql(
                "sale",
                con=self.db_connection.get_engine(),
                if_exists="replace",
                index=False,
                method="multi",
            )
            self.logger.log_info("Data loading completed successfully.")
        except Exception as e:
            self.logger.log_error(e)
            raise
