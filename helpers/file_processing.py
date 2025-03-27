# features/steps/file_processing.py
import os
import pandas as pd
import logging
from typing import Dict, Any



class FileProcessor:
    """Handles various file processing types (CSV, Excel)."""

    def __init__(self: Any, file_name: str, context: Any):
        self.file_name = file_name
        self.context = context
        self.file_path = self.get_data_path(file_name)

    def process(self: Any):
        """Process the file based on its type (CSV, Excel)."""
        try:
            if self.file_name.endswith(".csv"):
                self.read_csv()
            elif self.file_name.endswith(".xlsx"):
                self.read_excel()
            else:
                raise ValueError(f"Unsupported file type for {self.file_name}")
        except Exception as e:
            logging.error(f"Error processing file {self.file_name}: {str(e)}")
            raise  # Re-raise the exception to stop further execution

    def read_csv(self: Any):
        """Read CSV file and store in context."""
        encoding = self.detect_encoding(self.file_path)
        self.context.df = pd.read_csv(self.file_path, encoding=encoding)
        self.log_processing()

    def read_excel(self: Any):
        """Read Excel file and store in context."""
        self.context.df = pd.read_excel(self.file_path)
        self.log_processing()

    def log_processing(self: Any):
        """Log file processing and check if the file is empty."""
        if self.context.df.empty:
            raise ValueError(f"Loaded file {self.file_name} is empty.")
        logging.info(f"Successfully processed file: {self.file_name}")

    def detect_encoding(self: Any, file_path: Any):
        """Detect the file encoding."""
        with open(file_path, "rb") as file:
            raw_data = file.read(10000)  # Read the first 10000 bytes
        result = chardet.detect(raw_data)
        return result["encoding"]

    def get_data_path(self: Any, file_name: Any):
        """Get the file path from the base directory."""
        base_dir = "test_data/csv_files"  # This is where the files are located
        return os.path.join(base_dir, file_name)