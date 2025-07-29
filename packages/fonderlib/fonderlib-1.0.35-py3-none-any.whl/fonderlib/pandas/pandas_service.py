import os
import logging
import pandas as pd

from ..common.logger import get_logger


class PandasService:
    logger: logging.Logger = get_logger("Pandas Service", level="DEBUG")

    def __init__(self):
        self.df = None

    def initialize(self, file_name: str, sheet_name: str):
        self.logger.info("Pandas service: reeading file...")
        self.logger.info(f"Current directory: {os.getcwd()}")
        self.df = pd.read_excel(
            os.path.join(self.folder, file_name + ".xlsx"), sheet_name=sheet_name
        )
        return self.df

    def clean_sheet(self):
        # Drop rows with all white spaces
        self.df.dropna(axis=0, how="all")

        # Drop columns with all white spaces
        self.df.dropna(axis=1, how="all")

        # Transform columns to lowercase
        self.df.columns = self.df.columns.str.lower()

    def order_sheet_by_date(self, key: str, ascending=True):
        # Ensure data has field and is date time type
        self.df[key] = pd.to_datetime(self.df[key])

        # Order sheet by field
        self.df = self.df.sort_values(by=key, ascending=ascending)

        return self.df

    def trim_spaces(self):
        # Transform all string data to lowercase and remove blank spaces
        self.df = self.df.map(
            lambda x: x.strip().lower().replace(" ", "") if isinstance(x, str) else x
        )
