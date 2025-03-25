# features/steps/file_processing.py

import os
import pandas as pd
import logging


class FileProcessor:
    """Handles various file processing types (CSV, Excel)."""

    def __init__(self, file_name: str, context):
        self.file_name = file_name
        self.context = context
        self.file_path = self.get_data_path(file_name)

    def process(self):
        """Process the file based on its type (CSV, Excel)."""
        if self.file_name.endswith(".csv"):
            self.read_csv()
        elif self.file_name.endswith(".xlsx"):
            self.read_excel()
        else:
            raise ValueError(f"Unsupported file type for {self.file_name}")

    def read_csv(self):
        """Read CSV file and store in context."""
        encoding = self.detect_encoding(self.file_path)
        self.context.df = pd.read_csv(self.file_path, encoding=encoding)
        self.log_processing()

    def read_excel(self):
        """Read Excel file and store in context."""
        self.context.df = pd.read_excel(self.file_path)
        self.log_processing()

    def log_processing(self):
        """Log file processing."""
        if self.context.df.empty:
            raise ValueError(f"Loaded file {self.file_name} is empty.")
        logging.info(f"Processing file: {self.file_name}")

    def detect_encoding(self, file_path):
        """Detect the file encoding."""
        import chardet

        with open(file_path, "rb") as file:
            raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        return result["encoding"]

    def get_data_path(self, file_name):
        """Get the file path from the base directory."""
        return os.path.join("test_data/csv_files", file_name)
