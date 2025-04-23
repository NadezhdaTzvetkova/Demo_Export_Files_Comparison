# =================== Imports ===================
import os
import pandas as pd
import chardet
import hashlib
import psutil
import logging
import random
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool


try:
    from typing import (
        Any,
        Optional,
        Union,
        Tuple,
        Dict,
    )  # For static analysis tools only
except ImportError:
    # Python 2 compatibility fallback definitions
    # These will never be used in Python 3 with typing support
    Any = None  # type: ignore
    Optional = None  # type: ignore
    Union = None  # type: ignore
    Tuple = None  # type: ignore
    Dict = None  # type: ignore

# =================== Global Constants ===================

ISO_DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
historical_records = {}  # type: dict


# =================== Main Memory Usage Function ===================


def get_memory_usage() -> Tuple[float, float]:
    """
    Helper function to get the current memory usage in MB and percentage.
    Returns both the memory usage in MB and percentage.

    :return: tuple (memory_usage_mb, memory_usage_pct)
    """
    memory_info = psutil.virtual_memory()
    memory_usage_mb = memory_info.used / (1024 * 1024)  # Convert to MB
    memory_usage_pct = memory_info.percent  # Get the percentage of used memory

    # Log memory usage
    logging.info(
        "Current memory usage: %.2f MB, %.2f%%" % (memory_usage_mb, memory_usage_pct)
    )

    # Check if memory usage exceeds the warning threshold
    if memory_usage_pct > 80:
        logging.warning("Memory usage exceeds the threshold: %.2f%%" % memory_usage_pct)

    # Check if memory usage exceeds the error threshold (critical level)
    if memory_usage_pct > 90:
        logging.error(
            "CRITICAL: Memory usage exceeds critical threshold: %.2f%%"
            % memory_usage_pct
        )

    return memory_usage_mb, memory_usage_pct


def monitor_memory_usage_during_processing(file_name: str) -> None:
    """
    Monitors memory usage during the processing of large files and tracks performance.
    :return: None
    """
    # Get memory usage before processing
    memory_before, _ = get_memory_usage()

    # Simulate file processing logic here (replace with actual processing steps)
    logging.info("Starting file processing for %s" % file_name)

    # Simulate processing delay using datetime
    start_time = datetime.now()  # Correctly using datetime for Python 2.7
    processing_duration = timedelta(seconds=1)  # Simulating 1 second delay per file
    end_time = start_time + processing_duration

    while datetime.now() < end_time:
        pass  # Busy wait for the desired amount of time

    # Get memory usage after processing
    memory_after, _ = get_memory_usage()

    # Track memory usage during the processing
    memory_increase = memory_after - memory_before
    logging.info("Memory usage during processing: %.2f MB" % memory_increase)

    # Check if memory usage increase is significant (e.g., over 100MB)
    if memory_increase > 100:
        logging.warning(
            "Memory usage increased significantly during processing: %.2f MB"
            % memory_increase
        )


def handle_memory_usage_exceedance() -> None:
    """
    Handles situations where memory usage exceeds predefined thresholds during file processing.
    It can trigger alerts, stop processing, or suggest actions.
    :return: None
    """
    _, memory_usage_pct = get_memory_usage()

    # If memory usage exceeds 80%, issue a warning
    if memory_usage_pct > 80:
        logging.warning(
            "Memory usage is at %.2f%%. Consider optimizing file processing."
            % memory_usage_pct
        )

    # If memory usage exceeds 90%, stop the process and raise an exception
    if memory_usage_pct > 90:
        logging.error(
            "Critical memory usage detected at %.2f%%. Stopping further processing."
            % memory_usage_pct
        )
        raise SystemExit(
            "System has exceeded memory usage limits, terminating process."
        )


def monitor_system_performance(file_name: str) -> None:
    """
    Monitors overall system performance and resource usage.
    :param file_name: The name of the file to be logged during the performance monitoring.
    :return: None
    """
    if file_name is None:
        raise ValueError("File name cannot be None for system performance monitoring.")

    # Check CPU usage, memory usage, and other system metrics
    logging.info("Monitoring system performance for file: %s" % file_name)
    handle_memory_usage_exceedance()  # Call function to handle memory exceedance


def monitor_memory_usage(
    processing_context,  # type: Dict[str, Any]
    file_name=None,  # type: Optional[str]
):
    # type: (...) -> Tuple[float, float]
    """
    Main function to monitor memory usage, including calling helper functions.

    :param processing_context: Context for file processing (e.g., file details)
    :param file_name: Optional file name for logging purposes
    :return: Tuple of memory usage in MB and percentage
    """

    if file_name is None:
        raise ValueError("File name must not be None for memory monitoring.")

    # Monitor memory usage during file processing
    monitor_memory_usage_during_processing(file_name)

    # If memory usage exceeds threshold, handle accordingly
    monitor_system_performance(file_name)

    # Return the current memory usage
    return get_memory_usage()


# =================== File Handling Utilities ===================


def get_test_data_path(feature_folder, file_name):
    # type: (str, str) -> str
    base_dir = "test_data"
    return os.path.join(base_dir, feature_folder, file_name)


def read_bank_export_file(feature_folder, file_name, sheet_name=None):
    # type: (str, str, Optional[Union[str, int]]) -> pd.DataFrame
    file_path = get_test_data_path(feature_folder, file_name)
    if not os.path.exists(file_path):
        raise IOError("File not found: {}".format(file_path))

    if file_name.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError(
            "Unsupported file format. Only CSV and Excel files are supported."
        )


def load_bank_export_file(feature_folder, file_name, sheet_name=None):
    # type: (str, str, Optional[Union[str, int]]) -> pd.DataFrame
    """Loads the bank export file (CSV or Excel) into a DataFrame with error handling and logging."""

    # Construct file path
    file_path = os.path.join("test_data", feature_folder, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        logging.error(
            "Test file {0} not found in {1}".format(
                file_name, os.path.join("test_data", feature_folder)
            )
        )
        raise IOError(
            "Test file {0} not found in {1}".format(
                file_name, os.path.join("test_data", feature_folder)
            )
        )

    try:
        # Load CSV file
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
            logging.info("Processed CSV file: {0}".format(file_path))
            return df

        # Load Excel file
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logging.info("Processed Excel file: {0}".format(file_path))
            return df

        else:
            # Raise error for unsupported file format
            logging.error("Unsupported file format: {0}".format(file_name))
            raise ValueError("Unsupported file format for file: {0}".format(file_name))

    except Exception as e:
        # Log error if file reading fails and raise an exception
        logging.error("Error loading file {0}: {1}".format(file_name, str(e)))
        raise RuntimeError("Error loading file {0}: {1}".format(file_name, str(e)))


# =================== File Processor Class ===================
class FileProcessor(object):
    def __init__(self, file_name, context, feature_folder="csv_files"):
        # type: (str, Any, str) -> None
        self.file_name = file_name
        self.context = context
        self.feature_folder = feature_folder
        self.file_path = self.get_data_path(file_name)

    def process(self):
        # type: () -> None
        if self.is_supported_file_type():
            self.read_file()
        else:
            raise ValueError("Unsupported file type for {}".format(self.file_name))

    def read_file(self):
        # type: () -> None
        encoding = self.detect_encoding(self.file_path)  # type: str
        if self.file_name.endswith(".csv"):
            self.context.df = pd.read_csv(self.file_path, encoding=encoding)
        elif self.file_name.endswith(".xlsx"):
            self.context.df = pd.read_excel(self.file_path)
        self.log_processing()

    def log_processing(self):
        # type: () -> None
        if self.context.df.empty:
            raise ValueError("Loaded file {} is empty.".format(self.file_name))
        logging.info("Successfully processed file: {}".format(self.file_name))

    @staticmethod
    def detect_encoding(file_path):
        # type: (str) -> str
        with open(file_path, "rb") as file:
            raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        encoding = result.get("encoding") or "utf-8"  # fallback to UTF-8 if None
        return encoding

    def get_data_path(self, file_name):
        # type: (str) -> str
        base_dir = "test_data"
        feature_folder = self.feature_folder or "csv_files"
        return os.path.join(base_dir, feature_folder, file_name)

    def is_supported_file_type(self):
        # type: () -> bool
        return self.file_name.endswith(".csv") or self.file_name.endswith(".xlsx")


# =================== Shared Processing Utility ===================
def process_worker(q, context):
    # type: (Any, Any) -> None
    while not q.empty():
        file_path = q.get()
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
                logging.info("Processed CSV file: {}".format(file_path))
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path, sheet_name=None)
                logging.info("Processed Excel file: {}".format(file_path))
            else:
                raise ValueError("Unsupported file format: {}".format(file_path))

            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=0.5)
            while datetime.now() < end_time:
                pass

            context.processed_data[file_path] = df
        except Exception as e:
            logging.error("Failed to process {}: {}".format(file_path, str(e)))
            context.failed_files.append(file_path)
        finally:
            q.task_done()


# =================== File Processing Utilities ===================


def get_test_file_path(context, file_name):
    # type: (Any, str) -> str
    """
    Resolves the full path to the test data file based on:
    - The folder where the .feature file lives (e.g. financial_accuracy_tests)
    - The feature file name (e.g. basel_iii_capital_validation)
    - The expected test data folder structure:
        test_data/<feature_folder>_test_data/<feature_file>_test_data/<file_name>
    """

    feature_path = context.feature.filename
    feature_folder = os.path.basename(os.path.dirname(feature_path))
    feature_file = os.path.splitext(os.path.basename(feature_path))[0]

    test_data_path = os.path.join(
        "test_data",
        feature_folder.replace("_tests", "_test_data"),
        "{}_test_data".format(feature_file),
        file_name,
    )

    return test_data_path


def process_file(context, processing_type=None):
    # type: (Any, Any) -> None
    """Handles file processing based on the processing type."""

    # Simulate file processing delay using datetime
    simulated_delay = random.uniform(0.5, 2.0)
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=simulated_delay)
    while datetime.now() < end_time:
        pass  # Simulating processing delay

    def process_each_file(file_path):
        # type: (Any) -> pd.DataFrame
        """Processes files based on their type (CSV or Excel)."""
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            logging.info("Processed CSV file: {0}".format(file_path))
            return df
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path, sheet_name=None)
            logging.info("Processed Excel file: {0}".format(file_path))
            return df
        else:
            raise ValueError("Unsupported file format: {0}".format(file_path))

    # Handle different types of processing based on the processing_type
    if processing_type == "error-prone":
        context.error_count = (
            context.transaction_count * context.error_percentage
        ) // 100
        context.valid_transactions = context.transaction_count - context.error_count
        logging.info(
            "Processed {0} valid transactions from {1}.".format(
                context.valid_transactions, context.file_name
            )
        )

    elif processing_type == "concurrent":
        # Using ThreadPool from multiprocessing.pool
        pool = ThreadPool(processes=5)
        context.processed_files = pool.map(process_each_file, context.file_paths)

    elif processing_type == "column_validation":
        df = process_each_file(context.file_name)
        context.mismatched_columns = [
            col for col in context.expected_columns if col not in df.columns
        ]
        logging.info(
            "Processed {0}. Column mismatches detected: {1}".format(
                context.file_name, context.mismatched_columns
            )
        )

    elif processing_type == "format_validation":
        df = process_each_file(context.file_name)
        context.format_mismatches = [
            col
            for col in context.columns_to_check
            if not isinstance(df[col].dtype, str)
        ]
        logging.info(
            "Processed {0}. Format mismatches detected: {1}".format(
                context.file_name, context.format_mismatches
            )
        )

    elif processing_type == "extra_columns":
        df = process_each_file(context.file_name)
        context.extra_columns_detected = [
            col for col in df.columns if col not in context.expected_columns
        ]
        logging.info(
            "Processing {0}. Extra columns detected: {1}".format(
                context.file_name, context.extra_columns_detected
            )
        )

    elif processing_type == "header_validation":
        df = process_each_file(context.file_name)
        context.header_mismatch_detected = [
            col for col in context.expected_columns if col not in df.columns
        ]
        logging.info(
            "Processing {0}. Header mismatch detected: {1}".format(
                context.file_name, context.header_mismatch_detected
            )
        )

    elif processing_type == "merged_cells":
        if isinstance(context.file_name, str) and context.file_name.endswith(
            ".xlsx"
        ):  # Ensure it's a string
            df = pd.read_excel(context.file_name)
            context.merged_cells_detected = any(df.iloc[:, 0].isnull())
            logging.info(
                "Processing {0}. Merged cells detected: {1}".format(
                    context.file_name, context.merged_cells_detected
                )
            )

    else:
        df = process_each_file(context.file_name)
        context.process_result = "File processed successfully."
        logging.info("File {0} processed successfully.".format(context.file_name))


# =================== File Hashing ===================
def compute_file_hash(file_name):
    # type: (str) -> str
    return hashlib.md5(file_name.encode()).hexdigest()


# =================== Centralized File Comparison ===================
def compare_hashes(
    context, hash_to_compare, source_name="context.db_data", target_name=None
):
    # type: (Any, str, str, Optional[str]) -> bool
    start_time = datetime.now()
    source_hash = _get_source_hash(context, source_name)
    is_modified = source_hash != hash_to_compare
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    logging.info(
        "Comparison for {}: {} (Time taken: {:.2f} seconds)".format(
            target_name,
            "Discrepancy found" if is_modified else "No discrepancy",
            duration,
        )
    )

    return is_modified


def _get_source_hash(context, source_name):
    # type: (Any, str) -> str
    if source_name == "context.db_data":
        return context.db_data["hash"]
    elif source_name in context.resolved_issues:
        return context.resolved_issues[source_name]["hash"]
    elif source_name in historical_records:
        return historical_records[source_name]["hash"]
    else:
        raise ValueError(
            "Source {} not found in context or historical records.".format(source_name)
        )


# =================== Performance Validation ===================
def process_and_validate_performance(context, expected_time):
    # type: (Any, float) -> None
    logging.info(
        "Starting performance validation for {}: File count: {}, Year range: {}".format(
            context.file_name, context.file_count, context.year_range
        )
    )

    try:
        file_processor = FileProcessor(
            file_name=context.file_name, context=context
        )  # type: FileProcessor
        start_time = datetime.now()
        file_processor.process()
        elapsed_time = (datetime.now() - start_time).total_seconds()  # type: float

        if elapsed_time <= expected_time:
            logging.info(
                "Performance validation successful: Processed {} files in {:.2f} seconds.".format(
                    context.file_count, elapsed_time
                )
            )
        else:
            logging.warning(
                "Performance validation failed: Processed {} files in {:.2f} seconds, exceeds {} seconds.".format(
                    context.file_count, elapsed_time, expected_time
                )
            )
    except Exception as e:
        logging.error(
            "Error during performance validation for {}: {}".format(
                context.file_name, str(e)
            )
        )
